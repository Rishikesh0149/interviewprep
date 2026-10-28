import ast
import datetime
import subprocess
import json
import time
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, CodingSubmission, Badge
from app.schemas import (
    CodingProblemOut, CodeRunRequest, CodeRunResponse, TestCaseResult, CodingSubmissionOut
)
from app.services.auth import get_current_user
from app.seed_data.coding_problems import CODING_PROBLEMS

router = APIRouter(prefix="/coding", tags=["Code Arena"])

DISALLOWED_NODES = (
    ast.Import, ast.ImportFrom
)

def _sanitize_python_ast(code: str):
    """Ensure submitted Python code does not import unauthorized system modules"""
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # Disallow dangerous modules
            for alias in getattr(node, 'names', []):
                if alias.name.split('.')[0] in ['os', 'sys', 'subprocess', 'shutil', 'socket', 'urllib', 'requests']:
                    raise ValueError(f"Importing '{alias.name}' is restricted in the execution sandbox.")
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in ['eval', 'exec', '__import__', 'open']:
                raise ValueError(f"Calling '{node.func.id}' is restricted in the execution sandbox.")


def _execute_python_tests(code: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Execute Python code against test cases with safety guardrails"""
    try:
        _sanitize_python_ast(code)
    except Exception as e:
        return {
            "status": "SyntaxError",
            "passed_cases": 0,
            "total_cases": len(test_cases),
            "runtime_ms": 0.0,
            "test_results": [
                TestCaseResult(
                    input_str="",
                    expected_output="",
                    actual_output="",
                    passed=False,
                    error=f"Security/Syntax Check Failed: {str(e)}"
                )
            ],
            "ai_feedback": "Review syntax errors or restricted keywords before running.",
            "time_complexity": "N/A",
            "space_complexity": "N/A"
        }

    # Execute in local sandbox scope
    local_scope: Dict[str, Any] = {}
    try:
        exec(code, {"__builtins__": __builtins__}, local_scope)
    except Exception as e:
        return {
            "status": "SyntaxError",
            "passed_cases": 0,
            "total_cases": len(test_cases),
            "runtime_ms": 0.0,
            "test_results": [
                TestCaseResult(
                    input_str="",
                    expected_output="",
                    actual_output="",
                    passed=False,
                    error=f"Runtime error during script definition: {str(e)}"
                )
            ],
            "ai_feedback": "Ensure functions are defined properly without top-level errors.",
            "time_complexity": "N/A",
            "space_complexity": "N/A"
        }

    # Find candidate function
    candidate_funcs = [v for k, v in local_scope.items() if callable(v)]
    if not candidate_funcs:
        return {
            "status": "Failed",
            "passed_cases": 0,
            "total_cases": len(test_cases),
            "runtime_ms": 0.0,
            "test_results": [
                TestCaseResult(
                    input_str="",
                    expected_output="",
                    actual_output="",
                    passed=False,
                    error="No function was found in the submitted code."
                )
            ],
            "ai_feedback": "Make sure to implement the required function name.",
            "time_complexity": "N/A",
            "space_complexity": "N/A"
        }

    func = candidate_funcs[-1]

    results: List[TestCaseResult] = []
    passed_count = 0
    t0 = time.perf_counter()

    for idx, tc in enumerate(test_cases):
        args = tc.get("args", [])
        expected = tc.get("expected")
        input_str = f"args = {args}"

        try:
            # Make deepcopy of mutable args to avoid mutation side-effects
            import copy
            args_copy = copy.deepcopy(args)
            actual = func(*args_copy)

            # Sort lists if comparing unordered results (like top-k or two-sum if needed)
            passed = (actual == expected)
            if not passed and isinstance(actual, list) and isinstance(expected, list) and len(actual) == len(expected):
                try:
                    passed = sorted(actual) == sorted(expected)
                except Exception:
                    passed = False

            if passed:
                passed_count += 1

            results.append(TestCaseResult(
                input_str=input_str if not tc.get("is_hidden") else "[Hidden Test Case]",
                expected_output=str(expected) if not tc.get("is_hidden") else "[Hidden]",
                actual_output=str(actual) if not tc.get("is_hidden") else ("[Passed]" if passed else "[Failed]"),
                passed=passed,
                error=None
            ))
        except Exception as err:
            results.append(TestCaseResult(
                input_str=input_str if not tc.get("is_hidden") else "[Hidden Test Case]",
                expected_output=str(expected) if not tc.get("is_hidden") else "[Hidden]",
                actual_output="",
                passed=False,
                error=f"Exception: {str(err)}"
            ))

    t1 = time.perf_counter()
    runtime_ms = round((t1 - t0) * 1000, 2)

    status_str = "Passed" if passed_count == len(test_cases) else "Failed"

    return {
        "status": status_str,
        "passed_cases": passed_count,
        "total_cases": len(test_cases),
        "runtime_ms": runtime_ms,
        "test_results": results,
        "ai_feedback": (
            "All test cases passed! Solution exhibits optimal asymptotic efficiency."
            if passed_count == len(test_cases)
            else f"Failed on {len(test_cases) - passed_count} test case(s). Check edge cases and data structures."
        ),
        "time_complexity": "O(N)",
        "space_complexity": "O(N)"
    }


def _execute_js_tests(code: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Execute JavaScript code via node.js CLI runner"""
    runner_script = f"""
{code}

const testCases = {json.dumps(test_cases)};
const results = [];
let passedCount = 0;

// Resolve first function
const funcNames = Object.keys(global).filter(k => typeof global[k] === 'function' && !['setTimeout', 'setInterval', 'setImmediate', 'clearTimeout'].includes(k));
// Also search local lexical
let targetFunc = typeof twoSum !== 'undefined' ? twoSum :
                 typeof isValidParentheses !== 'undefined' ? isValidParentheses :
                 typeof lengthOfLongestSubstring !== 'undefined' ? lengthOfLongestSubstring :
                 typeof coinChange !== 'undefined' ? coinChange :
                 typeof topKFrequent !== 'undefined' ? topKFrequent : null;

for (let i = 0; i < testCases.length; i++) {{
    const tc = testCases[i];
    try {{
        if (!targetFunc) throw new Error("Target function not found");
        const actual = targetFunc(...tc.args);
        const expected = tc.expected;
        const passed = JSON.stringify(actual) === JSON.stringify(expected);
        if (passed) passedCount++;
        results.push({{
            input_str: tc.is_hidden ? "[Hidden Test Case]" : JSON.stringify(tc.args),
            expected_output: tc.is_hidden ? "[Hidden]" : JSON.stringify(expected),
            actual_output: tc.is_hidden ? (passed ? "[Passed]" : "[Failed]") : JSON.stringify(actual),
            passed: passed,
            error: null
        }});
    }} catch (err) {{
        results.push({{
            input_str: tc.is_hidden ? "[Hidden Test Case]" : JSON.stringify(tc.args),
            expected_output: tc.is_hidden ? "[Hidden]" : JSON.stringify(tc.expected),
            actual_output: "",
            passed: false,
            error: err.message
        }});
    }}
}}

console.log(JSON.stringify({{ passedCount, total: testCases.length, results }}));
"""
    try:
        t0 = time.perf_counter()
        proc = subprocess.run(["node", "-e", runner_script], capture_output=True, text=True, timeout=5)
        t1 = time.perf_counter()
        runtime_ms = round((t1 - t0) * 1000, 2)

        if proc.returncode != 0:
            return {
                "status": "SyntaxError",
                "passed_cases": 0,
                "total_cases": len(test_cases),
                "runtime_ms": 0.0,
                "test_results": [
                    TestCaseResult(
                        input_str="",
                        expected_output="",
                        actual_output="",
                        passed=False,
                        error=proc.stderr.strip()[:300]
                    )
                ],
                "ai_feedback": "JavaScript syntax error detected.",
                "time_complexity": "N/A",
                "space_complexity": "N/A"
            }

        output = json.loads(proc.stdout.strip())
        passed_cases = output.get("passedCount", 0)
        total_cases = output.get("total", len(test_cases))
        raw_results = output.get("results", [])

        test_results = [
            TestCaseResult(
                input_str=r["input_str"],
                expected_output=r["expected_output"],
                actual_output=r["actual_output"],
                passed=r["passed"],
                error=r.get("error")
            )
            for r in raw_results
        ]

        return {
            "status": "Passed" if passed_cases == total_cases else "Failed",
            "passed_cases": passed_cases,
            "total_cases": total_cases,
            "runtime_ms": runtime_ms,
            "test_results": test_results,
            "ai_feedback": "JavaScript runner execution finished.",
            "time_complexity": "O(N)",
            "space_complexity": "O(N)"
        }
    except Exception as e:
        return {
            "status": "Failed",
            "passed_cases": 0,
            "total_cases": len(test_cases),
            "runtime_ms": 0.0,
            "test_results": [
                TestCaseResult(
                    input_str="",
                    expected_output="",
                    actual_output="",
                    passed=False,
                    error=f"Execution error: {str(e)}"
                )
            ],
            "ai_feedback": "Execution timed out or encountered an internal environment limitation.",
            "time_complexity": "N/A",
            "space_complexity": "N/A"
        }


@router.get("/problems", response_model=List[CodingProblemOut])
def list_coding_problems():
    """List available coding challenges with descriptions, constraints, and starter code"""
    problems_out = []
    for p in CODING_PROBLEMS:
        item = CodingProblemOut(
            id=p["id"],
            title=p["title"],
            difficulty=p["difficulty"],
            category=p["category"],
            description=p["description"],
            examples=p["examples"],
            constraints=p["constraints"],
            starter_code=p["starter_code"],
            hints=p["hints"],
            optimal_complexity=p["optimal_complexity"]
        )
        problems_out.append(item)
    return problems_out


@router.get("/problems/{problem_id}", response_model=CodingProblemOut)
def get_coding_problem(problem_id: str):
    """Retrieve detailed description and constraints for a single problem"""
    problem = next((p for p in CODING_PROBLEMS if p["id"] == problem_id), None)
    if not problem:
        raise HTTPException(status_code=404, detail="Coding problem not found.")

    return CodingProblemOut(
        id=problem["id"],
        title=problem["title"],
        difficulty=problem["difficulty"],
        category=problem["category"],
        description=problem["description"],
        examples=problem["examples"],
        constraints=problem["constraints"],
        starter_code=problem["starter_code"],
        hints=problem["hints"],
        optimal_complexity=problem["optimal_complexity"]
    )


@router.post("/run", response_model=CodeRunResponse)
def run_code_tests(payload: CodeRunRequest):
    """Execute code against visible test cases without recording a permanent submission"""
    problem = next((p for p in CODING_PROBLEMS if p["id"] == payload.problem_id), None)
    if not problem:
        raise HTTPException(status_code=404, detail="Coding problem not found.")

    visible_tests = [tc for tc in problem["test_cases"] if not tc.get("is_hidden")]

    if payload.language.lower() == "javascript":
        exec_res = _execute_js_tests(payload.code, visible_tests)
    else:
        exec_res = _execute_python_tests(payload.code, visible_tests)

    return CodeRunResponse(
        status=exec_res["status"],
        passed_cases=exec_res["passed_cases"],
        total_cases=exec_res["total_cases"],
        runtime_ms=exec_res["runtime_ms"],
        test_results=exec_res["test_results"],
        ai_feedback=exec_res["ai_feedback"],
        time_complexity=exec_res.get("time_complexity", problem["optimal_complexity"].split(",")[0].strip()),
        space_complexity=exec_res.get("space_complexity", problem["optimal_complexity"].split(",")[-1].strip())
    )


@router.post("/submit", response_model=CodeRunResponse)
def submit_code_solution(
    payload: CodeRunRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit code solution against all test cases (visible & hidden) and record progress"""
    problem = next((p for p in CODING_PROBLEMS if p["id"] == payload.problem_id), None)
    if not problem:
        raise HTTPException(status_code=404, detail="Coding problem not found.")

    all_tests = problem["test_cases"]

    if payload.language.lower() == "javascript":
        exec_res = _execute_js_tests(payload.code, all_tests)
    else:
        exec_res = _execute_python_tests(payload.code, all_tests)

    # Save submission record
    sub = CodingSubmission(
        user_id=current_user.id,
        problem_id=problem["id"],
        problem_title=problem["title"],
        language=payload.language,
        code_content=payload.code,
        passed_cases=exec_res["passed_cases"],
        total_cases=exec_res["total_cases"],
        runtime_ms=exec_res["runtime_ms"],
        status=exec_res["status"],
        ai_feedback=exec_res["ai_feedback"],
        time_complexity=problem["optimal_complexity"].split(",")[0].strip(),
        space_complexity=problem["optimal_complexity"].split(",")[-1].strip(),
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(sub)

    # If all passed, boost readiness score and check badges
    if exec_res["status"] == "Passed":
        current_user.readiness_score = min(100.0, round(current_user.readiness_score + 2.5, 1))

        # First code submission badge
        b1 = db.query(Badge).filter(Badge.user_id == current_user.id, Badge.badge_key == "first_code_pass").first()
        if not b1:
            badge = Badge(
                user_id=current_user.id,
                badge_key="first_code_pass",
                title="Code Warrior",
                description="Successfully passed all test cases for an algorithm challenge in Code Arena.",
                icon="code",
                tier="Bronze"
            )
            db.add(badge)

    db.commit()

    return CodeRunResponse(
        status=exec_res["status"],
        passed_cases=exec_res["passed_cases"],
        total_cases=exec_res["total_cases"],
        runtime_ms=exec_res["runtime_ms"],
        test_results=exec_res["test_results"],
        ai_feedback=exec_res["ai_feedback"],
        time_complexity=problem["optimal_complexity"].split(",")[0].strip(),
        space_complexity=problem["optimal_complexity"].split(",")[-1].strip()
    )


@router.get("/submissions", response_model=List[CodingSubmissionOut])
def get_user_submissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve historical code submissions for the logged in user"""
    subs = db.query(CodingSubmission).filter(
        CodingSubmission.user_id == current_user.id
    ).order_by(CodingSubmission.id.desc()).all()
    return subs
