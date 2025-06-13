from abc import ABC,abstractmethod
from datetime import datetime
import uuid
class Plugin(ABC):
    def __init__(self,name,version,author,config):
        self.id = str(uuid.uuid4())
        self.name=name
        self.version=version
        self.author = author
        self.config = config
        self.createdAt = datetime.now()
    @abstractmethod
    def render(self,userid):
        pass
class WeatherPlugin(Plugin):
    def render(self,userid):
        print(f"{userid} Rendering weather for {self.name}")
class StocksPlugin(Plugin):
    def render(self,userid):
        print(f"{userid} Rendering stocks for {self.name}")
class PluginRepo:
    def __init__(self):
        self.storage={}
    def save(self,plugin:Plugin):
        if(plugin.name not in self.storage):
            self.storage[plugin.name] = []
        self.storage[plugin.name].append(plugin)
    def getLatest(self,name):
        return self.storage[name][-1] if name in self.storage else None
class PluginManager:
    def __init__(self,repo:PluginRepo):
        self.repo=repo
        self.loadedPlugins = {}
    def registerPlugin(self,plugin:Plugin):
        self.repo.save(plugin)
        self.loadedPlugins[plugin.name] = plugin
    def loadPlugin(self,name:str):
        return self.repo.getLatest(name)
class Dashboard:
    def __init__(self,userId):
        self.userId = userId
        self.widgets = []
    def addPlugin(self,plugin:Plugin):
        self.widgets.append(plugin)
    def renderPlugin(self):
        for plugin in self.widgets:
            plugin.render(self.userId)
repo = PluginRepo()
manager = PluginManager(repo)
weather = WeatherPlugin("WeatherPro", "1.0", "Vishali", {"units": "C"})
stocks = StocksPlugin("StockWatch", "1.0", "Aishu", {"exchange": "NASDAQ"})
manager.registerPlugin(weather)
manager.registerPlugin(stocks)
dashboard = Dashboard("123")
dashboard.addPlugin(manager.loadPlugin("WeatherPro"))
dashboard.addPlugin(manager.loadPlugin("StockWatch"))
dashboard.renderPlugin()
