"""Legacy shim for enqueue_job script."""

from backend.app.services.enqueue_job import enqueue_simple_job, main

if __name__ == "__main__":
    main()
