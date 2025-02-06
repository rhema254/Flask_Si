from Server.exts import db
import datetime
from sqlalchemy import ARRAY



"""" This is my database classes. They reprsent db tables """

class services(db.Enum):
    StrategyAutomation = "Strategy Automation"
    TestingAndOptimization = "Testing And Optimization"
    RiskManagementIntegration = "Risk Management Integration"
    TechnicalSupport = "Technical Support"      
    MultiPlatformDevelopment = "Multi-Platform Development"
    APIIntegrationServices = "API Integration Services"
    MachineLearningEnhancement = "Machine Learning Enhancement"
    MarketDataAnalysisTools = "Market Data Analysis Tools"


class Status(db.Enum):
    Scheduled = "Scheduled" 
    Done = "Done"
    Cancelled = "Cancelled"



class Booking(db.Model):
    """ The data attributes for each booking record """
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(10), nullable=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    timezone = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    meet_link = db.Column(db.String(60), nullable=True, default = 'none')
    status = db.Column(db.String(10), nullable=False, default = Status.Scheduled)
    created_at = db.Column(db.DateTime, default=db.func.now())
    services = db.Column(db.String(300), nullable=False)
    
    def __repr__(self):     
        return f" A Booking for {self.fullname} in timezone {self.timezone} on {self.date} at {self.time} for {self.services} "; 
    
    #Convenience Methods. 

    def save(self):
        db.session.add(self)
        db.session.commit()
               

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'services':
                if self.services and isinstance(self.services, list):
                    if value in self.services:
                        self.services.remove(value)
                else:
                    self.services = value
            else:
                setattr(self, key, value)
        
        self.save() 

