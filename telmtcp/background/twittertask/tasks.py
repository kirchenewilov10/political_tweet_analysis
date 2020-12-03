from background_task import background
from telmtcp.module.telmtcp import twitter as mtw

@background()
def process_twitter_data_update():
    mtw.update_twitter_analysis()