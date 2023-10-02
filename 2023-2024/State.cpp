class State{
    private:
        // Safe operating paramaters
        double voltage[2], velocity[2], temp[2];
    
    public:

        State(double voltLow, double voltHigh, double velLow, double velHigh, double tempLow, double tempHigh){
            voltage[0] = voltLow;
            voltage[1] = voltHigh;
            velocity[0] = velLow;
            velocity[1] = velHigh;
            temp[0] = tempLow;
            temp[1] = tempHigh;
        }

        double* getVoltRange(){
            return voltage;
        }
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
