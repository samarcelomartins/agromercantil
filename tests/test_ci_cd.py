from airflow.models import DagBag

def test_dag_integridade():
    dag_bag = DagBag()
    assert len(dag_bag.import_errors) == 0

def test_dag_task_count():
    dag_bag = DagBag()
    dag = dag_bag.get_dag(dag_id='meu_dag')
    assert len(dag.tasks) > 0
