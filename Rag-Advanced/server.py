from fastapi import FastAPI , Query
from .task_queue.connection import queue

from .task_queue.worker import process_query

app=FastAPI()

@app.get("/")
def chat():
    return {"message":"server is running"}


@app.post("/chat")
def chat(
    query: str = Query(..., description="The user's query")
):
    # query ko queue me daal do
    job = queue.enqueue(process_query, query)
     # fir user ko response do ki your query is being processed
    return {"message": "Your query is being processed", "job_id": job.id}
   
    # fir background me query ko process kro
    # fir user ko response do
    
@app.get("/results/{job_id}")
def get_results(job_id: str = Path(..., description="The job ID")):
        job = queue.fetch_job(job_id)
        if job is None:
            return {"message": "Job not found"}
        elif job.is_finished:
            return {"message": "Job completed", "result": job.result}
        elif job.is_queued:
            return {"message": "Job is still in the queue"}
        elif job.is_started:
            return {"message": "Job is being processed"}
        else:
            return {"message": "Job status unknown"}    

        