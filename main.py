from logger.init_system_loggers import init_sys_loggers
import uvicorn
import os

if os.getenv('ENVIRONMENT') == 'development':
    init_sys_loggers()

if __name__ == "__main__":
    uvicorn.run(
        "server.initialize_app:app",
        host="127.0.0.1",
        log_level="debug" if os.getenv(
            'ENVIRONMENT') == 'development' else "info",
        use_colors=True,
        log_config=None,
        reload=True
    )
