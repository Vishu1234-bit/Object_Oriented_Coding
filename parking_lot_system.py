from enum import Enum
import uuid
from datetime import datetime
import time
class VehicleType(Enum):
    BIKE="BIKE"
    CAR="CAR"
    TRUCK="Truck"
class Vehicle:
    def __init__(self,vehicleType,numberPlate):
        self.vehicleType = vehicleType
        self.numberPlate = numberPlate
class Slot:
    def __init__(self,slotId,vehicleType):
        self.vehicleType = vehicleType
        self.isAvailable = True
        self.slotId = slotId
    def assignVehicle(self,vehicle:Vehicle):
        self.isAvailable = False
    def vacateVehicle(self):
        self.isAvailable=True
class Ticket:
    def __init__(self,slot,vehicle):
        self.ticketId = str(uuid.uuid4())
        self.entry_time=datetime.now()
        self.exit_time=None
        self.vehicle = vehicle
        self.slot = slot
class Floor:
    def __init__(self,floorNo,slots):
        self.floorNo = floorNo
        self.slots = slots
    def getAvailableSlot(self,vehicleType):
        for slot in self.slots:
            if(slot.vehicleType==vehicleType and slot.isAvailable):
                return slot
        return None
class Payment:
    def __init__(self,ticket:Ticket):
        self.amount=self.calculateAmount(ticket)
        self.status='Pending'
    def calculateAmount(self,ticket):
        duration = (datetime.now()-ticket.entry_time).seconds/3600
        return round(duration*20,2)
    def makePayment(self):
        self.status='Paid'
class ParkingLot:
    def __init__(self,floors):
        self.floors=floors
        self.activeTickets={}
    def parkVehicle(self,vehicle):
        for floor in self.floors:
            slot = floor.getAvailableSlot(vehicle.vehicleType)
            if(slot):
                slot.assignVehicle(vehicle)
                ticket = Ticket(slot,vehicle)
                self.activeTickets[ticket.ticketId] = ticket
                return ticket
        raise Exception("No available slot")
    def unparkVehicle(self,ticketId):
        ticket = self.activeTickets.get(ticketId)
        if(not ticket):
            raise Exception('Invalid ticket')
        ticket.slot.vacateVehicle()
        ticket.exit_time =datetime.now()
        payment = Payment(ticket)
        payment.makePayment()
        del self.activeTickets[ticketId]
        return payment
slots_floor1 = [Slot("S1",VehicleType.CAR),Slot("S1",VehicleType.BIKE),Slot("S1",VehicleType.TRUCK)]
floor = Floor(1,slots_floor1)
lot = ParkingLot([floor])
car = Vehicle(VehicleType.CAR,'TN01AB1234')
ticket = lot.parkVehicle(car)
print("Vehicle parket,",ticket.ticketId)
time.sleep(2)
payment = lot.unparkVehicle(ticket.ticketId)
print("Vehicle unparked,amount paid",payment.status,payment.amount)
