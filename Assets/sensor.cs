using UnityEngine;
using System.IO.Ports;
using System.Threading;
using System.Collections.Generic;
using System.Timers;
using System.ComponentModel;
using System.Text;
using System;


public class sensor : MonoBehaviour
{
    [SerializeField]
    public string device = "/dev/ttyUSB0";
    SerialPort port;
    byte[] byteBuffer = new byte[18];
    float yaw_angle;
    float pitch_angle;
    float roll_angle;
    // Start is called before the first frame update
    void Start()
    {
    	port = new SerialPort(device, 115200, Parity.None, 8, StopBits.One);
    	port.Open();
        Thread t1 = new Thread(Update_data);
        t1.Start();
    }
    int twosComplement_hex(int hexval){
        int bits = 16;
        int val = hexval;
        if ((hexval & (1 << bits-1)) != 0){
            val -= 1 << bits;
        }
        return val;
    
    }
    
    void Update(){
    	
        transform.rotation = Quaternion.Euler(pitch_angle, -yaw_angle, -roll_angle);
    }

    // Update is called once per frame
    void Update_data()
    {
    	while(true){
	    	port.Read(byteBuffer, 0, 18);
	    	yaw_angle   = twosComplement_hex(byteBuffer[10] | byteBuffer[11] << 8) / 100.0f;
	    	pitch_angle = twosComplement_hex(byteBuffer[12] | byteBuffer[13] << 8) / 100.0f;
	    	roll_angle  = twosComplement_hex(byteBuffer[14] | byteBuffer[15] << 8) / 100.0f;
		Debug.Log(yaw_angle); 
    	}
    }
}
