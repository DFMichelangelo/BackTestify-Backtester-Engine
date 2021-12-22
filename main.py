from logger.init_system_loggers import init_sys_loggers
import uvicorn
import os
uvicorn_config = {
    "app": "server:app",
    "host": "127.0.0.1",
    "log_level": "debug",
    "use_colors": True,
}
if __name__ == "__main__":
    if os.getenv('ENVIRONMENT') == 'development':
        init_sys_loggers()
        uvicorn_config["log_config"] = None
        uvicorn_config["reload"] = True

    uvicorn.run(
        **uvicorn_config
    )
