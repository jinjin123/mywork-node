from fastapi import FastAPI,Request
from sqlalchemy import Boolean, Column, Integer, String,DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

SQLALCHEMY_DATABASE_URI:str = 'mysql+pymysql://root:zxc123@192.168.1.110:3306/jlpt'
engine = create_engine(SQLALCHEMY_DATABASE_URI,pool_pre_ping=True)
# 生成sessionlocal类，这个类的每一个实例都是一个数据库的会话
# 注意命名为SessionLocal，与sqlalchemy的session分隔开
SessionLocal = sessionmaker(autocommit=False,autoflush=True,bind=engine)
session = SessionLocal()
Base = declarative_base()

templates = Jinja2Templates(directory="templates") # 实例化Jinja2对象，并将文件夹路径设置为以templates命令的文件夹


# 模型类，tablename指表名，如果数据库中没有这个表会自动创建，有表则会沿用
class jlpt_info(Base):
    __tablename__ = "jlpt_member"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    mem_id = Column(String(20),nullable=False)
    mem_pwd = Column(String(20),nullable=False)
    level = Column(Integer,nullable=False)
    schoold_id = Column(Integer,default=0)
    schoold_name = Column(String(30),nullable=False)
    status = Column(Integer,nullable=True) # 0 register success | 1 fail
    lock = Column(Integer,default=0)  # 0 use | 1 not use
    submit_time = Column(DateTime)
    update_time = Column(DateTime)


Base.metadata.create_all(bind=engine)


@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
    mem_list = []
    mem = session.query(jlpt_info).all()
    session.close()
    for i in range(len(mem)):
        mem_list.append(
            {
                'mem_id':mem[i].mem_id,
                # 'mem_pwd':mem[i].mem_pwd,
                'level':mem[i].level,
                'schoold_id':mem[i].schoold_id,
                'schoold_name':mem[i].schoold_name,
                'status': mem[i].status,
                'lock': mem[i].lock,
                'submit_time': mem[i].submit_time,
                'update_time': mem[i].update_time,
            }
        )
    return templates.TemplateResponse("index.html", {"request": request, "mem_info": mem_list })

@app.get("/form",response_class=HTMLResponse)
async def summitform(request: Request):
        return templates.TemplateResponse("form.html", {"request": request })

@app.post("/items/", response_model=jlpt_info, tags=["items"])
async def create_item(item: jlpt_info):
    return item



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)