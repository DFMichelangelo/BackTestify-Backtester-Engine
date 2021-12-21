from logger.init_system_loggers import init_sys_loggers
import uvicorn

uvicorn_config = {
    "app": "server.app:app",
    "host": "127.0.0.1",
    "reload": True,
    "log_level": "debug",
    "use_colors": True,
}
if __name__ == "__main__":
    add_log_config = init_sys_loggers()
    if add_log_config:
        uvicorn_config["log_config"] = None
    uvicorn.run(
        **uvicorn_config
    )
