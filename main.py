import logging
import os
import time

from dotenv import load_dotenv
from google.cloud import workflows_v1
from google.cloud.workflows import executions_v1
from google.cloud.workflows.executions_v1 import Execution
from google.cloud.workflows.executions_v1.types import executions


def setup_logging() -> logging.Logger:
    """LOG_LEVEL 환경변수 기반으로 로깅을 설정합니다."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, log_level, logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


def execute_workflow(
    project_id: str,
    location: str,
    workflow_id: str,
    arguments: str | None = None,
) -> Execution:
    """Workflow를 실행하고 결과를 대기합니다.

    Args:
        project_id: Google Cloud 프로젝트 ID
        location: Workflow 위치 (예: us-central1)
        workflow_id: 실행할 Workflow ID
        arguments: Workflow에 전달할 인자 (JSON 문자열, 선택사항)

    Returns:
        실행 완료된 Execution 객체
    """
    logger = logging.getLogger(__name__)

    execution_client = executions_v1.ExecutionsClient()
    workflows_client = workflows_v1.WorkflowsClient()

    parent = workflows_client.workflow_path(project_id, location, workflow_id)
    logger.info("Workflow 경로: %s", parent)

    if arguments:
        execution = executions_v1.Execution(argument=arguments)
        response = execution_client.create_execution(
            parent=parent,
            execution=execution,
        )
        logger.info("Arguments와 함께 Execution 생성: %s", response.name)
    else:
        response = execution_client.create_execution(request={"parent": parent})
        logger.info("Execution 생성: %s", response.name)

    execution_finished = False
    backoff_delay = 1
    max_backoff = 60

    logger.info("결과 대기 중...")

    while not execution_finished:
        execution_result = execution_client.get_execution(
            request={"name": response.name}
        )
        execution_finished = (
            execution_result.state != executions.Execution.State.ACTIVE
        )

        if not execution_finished:
            logger.debug("대기 중... (다음 폴링까지 %d초)", backoff_delay)
            time.sleep(backoff_delay)
            backoff_delay = min(backoff_delay * 2, max_backoff)
        else:
            logger.info("Execution 완료 - 상태: %s", execution_result.state.name)
            logger.info("Execution 결과: %s", execution_result.result)

    return execution_result


def main() -> None:
    """환경변수를 로드하고 Workflow를 실행합니다."""
    load_dotenv()
    logger = setup_logging()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    workflow_id = os.getenv("WORKFLOW_ID")
    arguments = os.getenv("WORKFLOW_ARGUMENTS")

    if not project_id:
        logger.error("GOOGLE_CLOUD_PROJECT 환경변수가 설정되지 않았습니다.")
        raise ValueError("GOOGLE_CLOUD_PROJECT 환경변수가 필요합니다.")

    if not location:
        logger.error("GOOGLE_CLOUD_LOCATION 환경변수가 설정되지 않았습니다.")
        raise ValueError("GOOGLE_CLOUD_LOCATION 환경변수가 필요합니다.")

    if not workflow_id:
        logger.error("WORKFLOW_ID 환경변수가 설정되지 않았습니다.")
        raise ValueError("WORKFLOW_ID 환경변수가 필요합니다.")

    logger.info("Workflow 실행 시작")
    logger.info("프로젝트: %s, 위치: %s, Workflow: %s", project_id, location, workflow_id)

    if arguments:
        logger.info("Arguments: %s", arguments)

    result = execute_workflow(project_id, location, workflow_id, arguments)

    logger.info("Workflow 실행 완료")
    return result


if __name__ == "__main__":
    main()
