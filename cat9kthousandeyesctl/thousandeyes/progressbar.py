"""
Handle progressbar
"""
from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn


class Progressbar:
    """
    Parameters
    ----------
    host : str
        Host for descriptionn
    Returns
    -------
    pbar : obj
        Progressbar obj
    """

    def __init__(self, host):
        """ Create progressbar instance """
        self.host = host
        desc = TextColumn("{task.description}", table_column=Column(ratio=1))
        progress = BarColumn(bar_width=None, table_column=Column(ratio=1))
        time_elapsed = TimeElapsedColumn(table_column=Column())
        self.progress = Progress(
            desc,
            progress,
            "[white][progress.percentage]{task.percentage:>3.0f}%",
            time_elapsed,
            expand=True,
        )

    def update(self, success=False, error=False, stage=None, msg=None):
        """ Update progressbar """
        if error is True:
            self.progress.update(task_id=0, description=f"{self.host}:\t{msg}")
            return
        if success is True:
            self.progress.update(
                task_id=0, description=f"{self.host}:\t{msg.capitalize()}"
            )
            return
        self.progress.update(
            task_id=0, description=f"{self.host}:\t{stage.capitalize()}"
        )
        return
