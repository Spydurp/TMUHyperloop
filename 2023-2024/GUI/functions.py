class State:
    #Safe operating paramaters
    voltage = [0] * 2
    velocity = [0] * 2
    temp = [0] * 2
    
    voltLow = voltage[0]
    voltHigh = voltage[1]
    velLow = velocity[0]
    velHigh = velocity[1]
    tempLow = temp[0]
    tempHigh = temp[1]

    def getVoltRange():
        return voltage
        double* getVelRange(){
            return velocity;
        }
        double* getTempRange(){
            return temp;
        }
};

class Safe: public State{
    private:
        bool brakeCheck = true;
    
    public:

};

class Launch: public State{
    private:

    public:
};

class Running: public State{
    private:

    public:
};

class Braking: public State{
    private:

    public:
};

class Crawling: public State{
    private:

    public:
};

class Fault: public State{
    private:

    public:
};