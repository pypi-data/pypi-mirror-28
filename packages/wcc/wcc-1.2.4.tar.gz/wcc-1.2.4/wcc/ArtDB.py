from peewee import *

database = MySQLDatabase('artdb', **{'port': 3306, 'password': 'WikiReader1', 'host': 'rm-m5e1e89ru01nj4568io.mysql.rds.aliyuncs.com', 'user': 'dbreader'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Ads(BaseModel):
    cont = TextField()
    inc = PrimaryKeyField()

    class Meta:
        db_table = 'ads'

class Appcomt(BaseModel):
    aid = BigIntegerField(null=True)
    cato = CharField(index=True, null=True)
    comtc = IntegerField(null=True)
    content = TextField(null=True)
    cstamp = DateTimeField()
    ctime = IntegerField(null=True)
    earnc = IntegerField()
    eid = BigIntegerField(index=True, null=True)
    eidfrm = CharField()
    fairc = IntegerField()
    flag = IntegerField(null=True)
    gid = BigIntegerField()
    hatec = IntegerField(null=True)
    inc = BigIntegerField(primary_key=True)
    ip = CharField(null=True)
    ipadcode = IntegerField()
    ipaddr = CharField()
    lang = CharField()
    likec = IntegerField(null=True)
    lovec = IntegerField()
    m5d = CharField(index=True)
    media = CharField()
    pid = BigIntegerField()
    pidfrm = BigIntegerField()
    playc = IntegerField()
    price = IntegerField()
    rcmdc = IntegerField()
    reform_flag = IntegerField()
    rid = BigIntegerField(index=True)
    ridfrm = BigIntegerField()
    rprtc = IntegerField()
    sharc = IntegerField(null=True)
    share = TextField()
    sickc = IntegerField()
    sid = IntegerField()
    soldc = IntegerField()
    starc = IntegerField(null=True)
    tags = CharField(null=True)
    tidfrm = BigIntegerField(index=True)
    tlock = IntegerField()
    tmpl = CharField(null=True)
    uinfo = TextField()
    utime = IntegerField(null=True)
    viewc = IntegerField(null=True)
    vlot = FloatField()
    vtime = IntegerField()
    wardc = IntegerField(null=True)
    wwwfrm = CharField()

    class Meta:
        db_table = 'appcomt'
        indexes = (
            (('eid', 'cato', 'inc'), False),
            (('rcmdc', 'ctime'), False),
            (('rcmdc', 'vtime'), False),
            (('wwwfrm', 'ctime'), False),
            (('wwwfrm', 'rid', 'inc'), True),
            (('wwwfrm', 'tidfrm'), False),
            (('wwwfrm', 'tmpl', 'media', 'cato', 'vtime'), False),
        )

class Artbuy(BaseModel):
    aid = BigIntegerField()
    expire = IntegerField()
    inc = BigIntegerField(primary_key=True)
    tid = BigIntegerField()
    time = IntegerField()
    uid = BigIntegerField()

    class Meta:
        db_table = 'artbuy'
        indexes = (
            (('uid', 'tid'), True),
        )

class Artcato(BaseModel):
    brief = CharField()
    cato = CharField()
    cnt = IntegerField()
    enabled = IntegerField()
    inc = PrimaryKeyField()
    mlcato = CharField()
    tmpl = CharField()

    class Meta:
        db_table = 'artcato'

class Artcato2(BaseModel):
    brief = CharField()
    cato = CharField()
    cnt = IntegerField()
    enabled = IntegerField()
    inc = PrimaryKeyField()
    mlcato = CharField()
    tmpl = CharField()

    class Meta:
        db_table = 'artcato2'

class Artcomt0(BaseModel):
    aid = BigIntegerField(null=True)
    cato = CharField(index=True, null=True)
    comtc = IntegerField(null=True)
    content = TextField(null=True)
    cstamp = DateTimeField()
    ctime = IntegerField(null=True)
    earnc = IntegerField()
    eid = BigIntegerField(index=True, null=True)
    eidfrm = CharField()
    fairc = IntegerField()
    flag = IntegerField(null=True)
    gid = BigIntegerField()
    hatec = IntegerField(null=True)
    inc = BigIntegerField(primary_key=True)
    ip = CharField(null=True)
    ipadcode = IntegerField()
    ipaddr = CharField()
    lang = CharField()
    likec = IntegerField(null=True)
    lovec = IntegerField()
    m5d = CharField(index=True)
    media = CharField()
    pid = BigIntegerField()
    pidfrm = BigIntegerField()
    playc = IntegerField()
    price = IntegerField()
    rcmdc = IntegerField()
    reform_flag = IntegerField()
    rid = BigIntegerField(index=True)
    ridfrm = BigIntegerField()
    rprtc = IntegerField()
    sharc = IntegerField(null=True)
    share = TextField()
    sickc = IntegerField()
    sid = IntegerField()
    soldc = IntegerField()
    starc = IntegerField(null=True)
    tags = CharField(null=True)
    tidfrm = BigIntegerField(index=True)
    tlock = IntegerField()
    tmpl = CharField(null=True)
    uinfo = TextField()
    utime = IntegerField(null=True)
    viewc = IntegerField(null=True)
    vlot = FloatField()
    vtime = IntegerField()
    wardc = IntegerField(null=True)
    wwwfrm = CharField()

    class Meta:
        db_table = 'artcomt0'
        indexes = (
            (('eid', 'cato', 'inc'), False),
            (('wwwfrm', 'ctime'), False),
            (('wwwfrm', 'rid', 'inc'), True),
            (('wwwfrm', 'tidfrm'), False),
        )

class Artdata0(BaseModel):
    aid = BigIntegerField(null=True)
    cato = CharField(index=True, null=True)
    comtc = IntegerField(null=True)
    content = TextField(null=True)
    cstamp = DateTimeField()
    ctime = IntegerField(null=True)
    earnc = IntegerField()
    eid = BigIntegerField(index=True, null=True)
    eidfrm = CharField()
    fairc = IntegerField()
    flag = IntegerField(null=True)
    gid = BigIntegerField()
    hatec = IntegerField(null=True)
    hot = IntegerField()
    inc = BigIntegerField(primary_key=True)
    ip = CharField(null=True)
    ipadcode = IntegerField()
    ipaddr = CharField()
    isample = IntegerField()
    lang = CharField()
    likec = IntegerField(null=True)
    lovec = IntegerField()
    m5d = CharField(index=True)
    media = CharField()
    mlstate = IntegerField(index=True)
    pid = BigIntegerField()
    pidfrm = BigIntegerField()
    playc = IntegerField()
    price = IntegerField()
    rcd = IntegerField()
    rcmdc = IntegerField()
    rid = BigIntegerField(index=True)
    ridfrm = BigIntegerField()
    rprtc = IntegerField()
    score = IntegerField()
    scr = IntegerField()
    sharc = IntegerField(null=True)
    share = TextField()
    sickc = IntegerField()
    sid = IntegerField()
    soldc = IntegerField()
    starc = IntegerField(null=True)
    tags = TextField(index=True, null=True)
    tidfrm = BigIntegerField(index=True)
    tlock = IntegerField()
    tmpl = CharField(null=True)
    uinfo = TextField()
    utime = IntegerField(null=True)
    viewc = IntegerField(null=True)
    vlot = FloatField()
    vtime = IntegerField()
    wardc = IntegerField(null=True)
    words = TextField()
    wwwfrm = CharField()

    class Meta:
        db_table = 'artdata0'
        indexes = (
            (('eid', 'cato', 'inc'), False),
            (('rcmdc', 'ctime'), False),
            (('rcmdc', 'vtime'), False),
            (('tmpl', 'cato', 'inc', 'isample', 'mlstate'), False),
            (('tmpl', 'cato', 'wwwfrm', 'ctime', 'vtime', 'scr', 'rcd', 'hot'), False),
            (('tmpl', 'wwwfrm', 'inc'), False),
            (('wwwfrm', 'ctime'), False),
            (('wwwfrm', 'rid', 'inc'), True),
            (('wwwfrm', 'tidfrm'), False),
        )

class Artdatax(BaseModel):
    aid = BigIntegerField(null=True)
    cato = CharField(index=True, null=True)
    comtc = IntegerField(null=True)
    content = TextField(null=True)
    createtimedt = DateTimeField()
    ctime = IntegerField(null=True)
    eid = BigIntegerField(index=True, null=True)
    eidfrm = CharField()
    fairc = IntegerField()
    flag = IntegerField(null=True)
    gem = IntegerField(null=True)
    gid = BigIntegerField()
    hatec = IntegerField(null=True)
    hitdc = IntegerField()
    inc = BigIntegerField(primary_key=True)
    ip = CharField(null=True)
    likec = IntegerField(null=True)
    lovec = IntegerField()
    media = CharField()
    pid = BigIntegerField()
    pidfrm = BigIntegerField()
    reform_flag = IntegerField()
    rid = BigIntegerField(index=True)
    ridfrm = BigIntegerField()
    sharc = IntegerField(null=True)
    share = TextField()
    sickc = IntegerField()
    sid = IntegerField()
    starc = IntegerField(null=True)
    tags = CharField(null=True)
    tidfrm = BigIntegerField()
    tmpl = CharField(null=True)
    utime = IntegerField(null=True)
    viewc = IntegerField(null=True)
    vlot = FloatField()
    vtime = IntegerField()
    wwwfrm = CharField()

    class Meta:
        db_table = 'artdatax'
        indexes = (
            (('tidfrm', 'wwwfrm'), True),
        )

class Artinc(BaseModel):
    inc = PrimaryKeyField()

    class Meta:
        db_table = 'artinc'

class Artlog(BaseModel):
    act = CharField()
    aid = BigIntegerField()
    ctime = IntegerField()
    dua = BigIntegerField(db_column='dua_id')
    inc = BigIntegerField(primary_key=True)
    param = IntegerField()
    stamp = DateTimeField()
    tid = BigIntegerField()
    uid = BigIntegerField()
    utime = IntegerField()
    wwwfrm = CharField()

    class Meta:
        db_table = 'artlog'
        indexes = (
            (('dua', 'tid', 'act', 'ctime'), False),
        )

class Artmenu(BaseModel):
    artcd = IntegerField()
    brief = TextField(null=True)
    cato = CharField()
    channel = CharField()
    ctime = IntegerField()
    delay = IntegerField()
    enabled = IntegerField()
    frmlostc = IntegerField()
    hot0 = IntegerField()
    hot1 = IntegerField()
    hot2 = IntegerField()
    hot3 = IntegerField()
    hot4 = IntegerField()
    hot5 = IntegerField()
    inc = PrimaryKeyField()
    latec = IntegerField()
    newqpu = IntegerField()
    newreqc = IntegerField()
    newresc = IntegerField()
    oldqpu = IntegerField()
    oldreqc = IntegerField()
    oldresc = IntegerField()
    portrait = CharField()
    rcd0 = IntegerField()
    rcd1 = IntegerField()
    rcd2 = IntegerField()
    rcd3 = IntegerField()
    rcd4 = IntegerField()
    rcd5 = IntegerField()
    scr0 = IntegerField()
    scr1 = IntegerField()
    scr2 = IntegerField()
    scr3 = IntegerField()
    scr4 = IntegerField()
    scr5 = IntegerField()
    tlock = IntegerField()
    tmpl = CharField()
    ucnt = IntegerField()
    utime = IntegerField()

    class Meta:
        db_table = 'artmenu'

class Arttag(BaseModel):
    brief = TextField()
    cato = CharField()
    enabled = IntegerField()
    inc = PrimaryKeyField()
    mltag = CharField()
    tag = CharField()
    tagtype = CharField()

    class Meta:
        db_table = 'arttag'
        indexes = (
            (('cato', 'tagtype', 'tag'), True),
        )

class Arttmap(BaseModel):
    cnt = BigIntegerField(null=True)
    inc = PrimaryKeyField()
    tix = IntegerField()

    class Meta:
        db_table = 'arttmap'

class Artview(BaseModel):
    channel = CharField(null=True)
    cpp = BigIntegerField()
    ctamp = DateTimeField()
    ctime = IntegerField()
    datas = TextField()
    eid = BigIntegerField()
    gid = BigIntegerField()
    inc = BigIntegerField(primary_key=True)
    lang = CharField()
    m5d = CharField()
    pid = BigIntegerField()
    portrait = CharField()
    rid = BigIntegerField()
    sid = IntegerField()
    stats = CharField()
    tid = BigIntegerField()
    tmpl = CharField()
    user = CharField()
    utime = IntegerField()
    vid = BigIntegerField()

    class Meta:
        db_table = 'artview'

class Channel(BaseModel):
    brief = CharField(null=True)
    catopfxs = CharField()
    code = CharField(null=True, unique=True)
    enabled = IntegerField()
    grp = IntegerField()
    inc = PrimaryKeyField()
    inlay = IntegerField()
    name = CharField()

    class Meta:
        db_table = 'channel'

class Classfier(BaseModel):
    accuracy = FloatField()
    cdate = IntegerField()
    classfier = CharField()
    conf = TextField()
    cstamp = DateTimeField()
    inc = BigIntegerField(primary_key=True)
    param = TextField()
    predictcost = IntegerField()
    rows = IntegerField()
    rowstrain = IntegerField()
    sample = CharField()
    tool = CharField()
    traincost = IntegerField()

    class Meta:
        db_table = 'classfier'

class Cnnpmc(BaseModel):
    channel = CharField()
    date = IntegerField()
    datetype = CharField()
    inc = BigIntegerField(primary_key=True)
    reqc = IntegerField()
    resc = IntegerField()
    rpr = FloatField()
    ustamp = DateTimeField()

    class Meta:
        db_table = 'cnnpmc'
        indexes = (
            (('channel', 'date'), True),
        )

class Cnnslot(BaseModel):
    artk = IntegerField()
    channel = CharField(null=True, unique=True)
    gap = IntegerField()
    inc = PrimaryKeyField()
    note = TextField(null=True)
    portrait = CharField()
    slotk = IntegerField()
    type = CharField()

    class Meta:
        db_table = 'cnnslot'

class Frmfilter(BaseModel):
    cato = CharField()
    cd = IntegerField()
    cnt = IntegerField()
    enabled = IntegerField()
    inc = PrimaryKeyField()
    tmpl = CharField()
    ucount = IntegerField()
    utime = IntegerField()
    wwwfrm = CharField()

    class Meta:
        db_table = 'frmfilter'
        indexes = (
            (('tmpl', 'cato'), False),
            (('tmpl', 'cato', 'wwwfrm'), True),
        )

class Furlinfo(BaseModel):
    cstamp = DateTimeField()
    ctime = IntegerField()
    datmd5 = CharField(unique=True)
    fps = FloatField()
    givsiz = IntegerField()
    givurl = CharField()
    h = IntegerField()
    inc = BigIntegerField(primary_key=True)
    lot = IntegerField()
    mime = CharField()
    ossurl = CharField()
    s = IntegerField()
    url = CharField()
    urlmd5 = CharField(unique=True)
    vdef = CharField()
    w = IntegerField()
    webpurl = CharField()

    class Meta:
        db_table = 'furlinfo'

class Infer(BaseModel):
    cato = CharField()
    genre = CharField()
    inc = BigIntegerField(primary_key=True)
    inferred = CharField(null=True)
    others = CharField(null=True)
    sayer = CharField()
    trope = CharField()
    type = CharField()
    what = CharField()
    wher = CharField()
    whn = CharField()
    who = CharField()
    why = CharField()
    word = CharField()

    class Meta:
        db_table = 'infer'
        indexes = (
            (('cato', 'word'), True),
        )

class Menupmc(BaseModel):
    cato = CharField()
    channel = CharField()
    date = IntegerField()
    inc = PrimaryKeyField()
    latec = IntegerField()
    newc = IntegerField()
    oldc = IntegerField()
    portrait = CharField()
    reqc = IntegerField()
    resc = IntegerField()
    ucnt = IntegerField()

    class Meta:
        db_table = 'menupmc'
        indexes = (
            (('date', 'channel', 'portrait', 'cato'), True),
        )

class Portrait(BaseModel):
    brief = TextField()
    code = CharField()
    enabled = IntegerField()
    inc = PrimaryKeyField()
    name = CharField()

    class Meta:
        db_table = 'portrait'

class Tidfrm(BaseModel):
    tidfrm = BigIntegerField(unique=True)

    class Meta:
        db_table = 'tidfrm'
        primary_key = False

class Usrlock(BaseModel):
    inc = PrimaryKeyField()
    tlock = IntegerField(null=True)
    uid = BigIntegerField(null=True, unique=True)

    class Meta:
        db_table = 'usrlock'

class Usrtag(BaseModel):
    action = CharField()
    cnt = IntegerField()
    date = IntegerField()
    inc = BigIntegerField(primary_key=True)
    tag = CharField()
    uid = BigIntegerField()

    class Meta:
        db_table = 'usrtag'

class Wcclist(BaseModel):
    author = CharField()
    author_avatar = TextField()
    author_name = CharField()
    author_tel = BigIntegerField()
    author_uid = IntegerField()
    avatar = TextField()
    catos = CharField()
    code = CharField(unique=True)
    cstamp = DateTimeField()
    ctime = IntegerField()
    enabled = IntegerField()
    hour = CharField()
    inc = BigIntegerField(primary_key=True)
    mdurl = CharField()
    name = CharField(unique=True)
    note = TextField()
    rtime = IntegerField()
    site = CharField(unique=True)
    state = CharField()
    uid = BigIntegerField()
    usolo = IntegerField()

    class Meta:
        db_table = 'wcclist'

class Wccpmc(BaseModel):
    date = IntegerField()
    datetype = CharField()
    e = IntegerField()
    eu = IntegerField()
    i = IntegerField()
    inc = BigIntegerField(primary_key=True)
    iu = IntegerField()
    m = IntegerField()
    type = CharField()
    wwwfrm = CharField()
    x = IntegerField()
    xu = IntegerField()

    class Meta:
        db_table = 'wccpmc'
        indexes = (
            (('wwwfrm', 'type', 'date'), True),
        )

class Wccpmc2(BaseModel):
    date = IntegerField()
    datetype = CharField()
    e = IntegerField()
    eu = IntegerField()
    i = IntegerField()
    inc = BigIntegerField(primary_key=True)
    iu = IntegerField()
    m = IntegerField()
    type = CharField()
    wwwfrm = CharField()
    x = IntegerField()
    xu = IntegerField()

    class Meta:
        db_table = 'wccpmc2'
        indexes = (
            (('wwwfrm', 'type', 'date'), True),
        )

