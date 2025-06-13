from datetime import datetime
class FlagConfig:
    def __init__(self,environments,users,rolloutpercent,roles,enabled):
        self.environments = environments
        self.users = users
        self.rolloutpercent = rolloutpercent
        self.roles = roles
        self.enabled=enabled
class FeatureFlag:
    def __init__(self,name,config:FlagConfig,createdAt=None,version=1):
        self.name=name
        self.version=version
        self.config = config
        self.createdAt = createdAt or datetime.now()
class RolloutStrategy:
    @staticmethod
    def isEnabledForUser(userId,percent):
        bucket = int(hashlib.sha256(userId.encode()).hexdigest,16)%100
        return bucket<=percent
class FlagRepo:
    def __init__(self):
        self.flags = {}
    def save(self,flag:FeatureFlag):
        if(flag.name not in self.flags):
            self.flags[flag.name]=[]
        flag.version = len(self.flags[flag.name])-1
        self.flags[flag.name].append(flag)
    def getLatest(self,name):
        return self.flags[name][-1] if name in self.flags else None
    def rollback(self,name,version):
        if(name in self.flags and 0<=version<len(self.flags[flag.name])):
            self.flags[flag.name].append(self.flags[name][version-1])
class FeatureFlagService:
    def __init__(self,repo:FlagRepo):
        self.repo = repo
    def isEnabled(self,featurename,env,userid,role,percent):
        flag = self.repo.getLatest(featurename)
        if(not flag):
            return False
        config = flag.config
        if(env not in config.environments):
            return False
        if(role in config.roles):
            return True
        if(config.rolloutpercent):
            return RolloutStrategy.isEnabledForUser(userid,percent)
        return config.isEnabled
    def createFlag(self,name,flagConfig:FlagConfig):
        self.repo.save(FeatureFlag(name,flagConfig))
    def rolloutFlag(self,name,version):
        self.repo.rollback(name,version)
flagConfig = FlagConfig(
environments=['prod','si','uat','si-dev'],
users=['vishali','aishu'],
rolloutpercent = 20,
roles=['dev','test'],
enabled=True
)
repo = FlagRepo()
service = FeatureFlagService(repo)
service.createFlag('search',flagConfig)
print(service.isEnabled('search','prod','vishali','dev',15))
for fname,fversion in repo.flags.items():
    print(f'{fname}-{fversion}')

            
