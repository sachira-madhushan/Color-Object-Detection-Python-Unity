using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System;

public class Color_Command_Receiver : MonoBehaviour
{
    private string command = "";
    Thread receiveThread;
    UdpClient client;
    int port;
    float com;
    public GameObject player;
    String move;
    void Start()
    {
        port = 22222;
        InitUDP();
    }
    private void InitUDP()
    {
        print("UDP Initialized");

        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();

    }
    private void ReceiveData()
    {
        client = new UdpClient(port);
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), port);
                byte[] data = client.Receive(ref anyIP);

                command = Encoding.UTF8.GetString(data);
                com = float.Parse(command)%3;
                
            }
            catch (Exception e)
            {
                print(e.ToString());
            }
         } 
    }
    void FixedUpdate()
    {
        player.transform.position = new Vector3(-1*com * Time.timeScale, 0, 0);
    }
        
    
}
