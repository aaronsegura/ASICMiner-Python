import blade, argparse, re, socket, pprint

pp = pprint.PrettyPrinter()

def parseArgs():

  parser = argparse.ArgumentParser(description="Tool to manipulate BitFountain ASICMINER v2 Blades", epilog=epilog)
  actionGroup = parser.add_mutually_exclusive_group()
  actionGroup.add_argument("-S", dest="Switch", action="store_true", help="Switch Servers")
  actionGroup.add_argument("-U", dest="Update", action="store_true", help="Update Configuration")
  actionGroup.add_argument("-v", dest="Verbose", action="store_true", help="Display all details about blade(s)")
  updateGroup = parser.add_argument_group(description="Update Flags:")
  updateGroup.add_argument("--address", dest="userAddress", metavar="<address>", help="IP Address")
  updateGroup.add_argument("--netmask", dest="userNetmask", metavar="<netmask>", help="Netmask")
  updateGroup.add_argument("--gw", dest="userGateway", metavar="<address>", help="Gateway")
  updateGroup.add_argument("--pdns", dest="userPDNS", metavar="<host", help="Primary DNS Server")
  updateGroup.add_argument("--sdns", dest="userSDNS", metavar="<host", help="Secondary DNS Server")
  updateGroup.add_argument("--phost", dest="userPHost", metavar="<host:port>", help="Primaryy Mining Server")
  updateGroup.add_argument("--puser", dest="userPUser", metavar="<user:pass>", help="Primary Server Credentials")
  updateGroup.add_argument("--shost", dest="userSHost", metavar="<host:port>", help="Secondary Mining Server")
  updateGroup.add_argument("--suser", dest="userSUser", metavar="<user:pass>", help="Secondary Server Credentials")
  updateGroup.add_argument("--webport", dest="userWebport", metavar='<port>', help="Web UI Listening Port")
  parser.add_argument("hostPort", nargs="+", metavar="host:port", help="Target Blade IPs")

  return parser.parse_args()

def main():
  args = parseArgs()
  #pp.pprint(args)
  x = ''
  updateList = {}

  newPHost = None
  newSHost = None
  newPUser = None
  newSUser = None

  if args.Update:
    ################################################3
    #
    # Always make sure your optics are clean
    #
    if args.userAddress:
      sock = ''

      try:
        sock = socket.inet_pton(socket.AF_INET, args.userAddress)
      except socket.error:
        print "Invalid Address: %s" % args.userAddress
        return False
      except NoneType:
        print "Invalid response from Blade"
        return False
      else:
        updateList["JMIP"] = args.userAddress

    ################################################3
    if args.userNetmask:
      x = re.search("^[1-2]{1}[2,4,5,9]{1}[0,2,4,5,8]{1}\.[0-2]{1}[0,2,4,5,9]{1}[0,2,4,5,8]{1}\.[0-2]{1}[0,2,4,5,9]{1}[0,2,4,5,8]{1}\.[0-9]{1,3}$", args.userNetmask)
      if not x:
        print "Invalid Netmask: %s" % args.userNetmask
        return False
      else:
        updateList["JMSK"] = args.userNetmask

    ################################################3
    if args.userPDNS:
      sock = ''

      try:
        sock = socket.inet_pton(socket.AF_INET, args.userPDNS)
      except socket.error:
        print "Invalid Address: %s" % args.userPDNS
        return False
      else:
        updateList["PDNS"] = args.userPDNS

    ################################################3
    if args.userSDNS:
      sock = ''

      try:
        sock = socket.inet_pton(socket.AF_INET, args.userSDNS)
      except socket.error:
        print "Invalid Address: %s" % args.userSDNS
        return False
      else:
        updateList["SDNS"] = args.userSDNS

    ################################################3
    if args.userPHost:
      sock = ''
      try:
        host, port = args.userPHost.split(":")
      except ValueError:
        print "MAlformed Host Specification: %s\nValid Format is: host:port" % args.userPHost
        return False

      resolved = ''
      try:
        resolved = socket.gethostbyname(host)
      except socket.gaierror, err:
        print "%s" % err.message

      try:
        sock = socket.inet_pton(socket.AF_INET, resolved)
      except socket.error:
        print "Invalid Address: %s" % host
        return False

      try:
        if int(port) < 0 or int(port) > 65535:
          print "Invalid Primary Host Port: %s" % port
      except (ValueError, TypeError):
        print "Malformed Primary Host Port: %s" % port
        return False

      newPHost = args.userPHost.split(":")

    ################################################3
    if args.userSHost:
      host = port = sock = None
      try:
        host, port = args.userSHost.split(":")
      except ValueError:
        print "MAlformed Host Specification: %s\nValid Format is: host:port" % args.userSHost
        return False

      resolved = ''
      try:
        resolved = socket.gethostbyname(host)
      except socket.gaierror, err:
        print "%s" % err.message

      try:
        sock = socket.inet_pton(socket.AF_INET, host)
      except socket.error:
        print "Invalid Address: %s" % host
        return False

      try:
        if int(port) < 0 or int(port) > 65535:
          print "Invalid Secondary Host Port: %s" % port
          return False
      except ValueError:
        print "Malformed Secondary Host Port: %s" % port
        return False

      newSHost = args.userSHost.split(":")

    ################################################3
    if args.userWebport:
      try:
        int(args.userWebport)
      except ValueError:
        print "MAlformed WebPort: %s" % args.userWebport
        return False

      if int(args.userWebport) < 0 or int(args.userWebport) > 65535:
        print "Invalid Webport: %s" % args.userWebport
        return False

      updateList["WPRT"] = args.userWebport

    ################################################3
    if args.userGateway:
      try:
        sock = socket.inet_pton(socket.AF_INET, args.userGateway)
      except socket.error:
        print "Invalid Gateway: %s" % args.userGateway
        return False

      updateList["JGTW"] = args.userGateway

    ################################################3
    if args.userPUser:
      if not re.search("^\S*:\S*$", args.userPUser):
        print "Invalid User String: %s\nValid Format: user:pass" % args.userPUser
        return False

      newPUser = args.userPUser

    ################################################3
    if args.userSUser:
      if not re.search("^\S*:\S*$", args.userSUser):
        print "Invalid User String: %s\nValid Format: user:pass" % args.userSUser
        return False

      newSUser = args.userSUser


  ################################################3
  #
  # Fire in the hole
  #
  for userBlade in args.hostPort:
    try:
      x = blade.Blade(userBlade)
    except blade.BladeError, err:
      print "[%s] Error: %s" % (userBlade, err.msg)
    else:

      if not args.Switch and not args.Update:
        if not args.Verbose:
          print "[%s:%s] %s @ %s MH/s, up %s days" % (x.address, x.webport, x.currentServer, x.MHPS, "%0.2f" % (x.uptime/86400))
        else:
          print "[%s:%s]\nCurrent Server: %s @ %s MH/S" % ( x.address, x.webport, x.currentServer, x.MHPS)
          print "Primary Host:   %s:%s, Login: %s" % (x.phost, x.pport, x.puser)
          print "Secondary Host: %s:%s, Login: %s" % (x.shost, x.sport, x.suser)
          print "DNS Servers:    %s, %s" % (x.pdns, x.sdns)
          print ""

      if args.Switch:
        try:
          x.switchServer()
        except blade.BladeError, err:
          print "[%s] Error Switching Servers: %s" % (userBlade, err.msg)
        else:
          print "[%s] Switched Server" % userBlade

      if args.Update:
        if newPHost and newSHost:
          updateList["MURL"] = "%s,%s" % (newPHost[0], newSHost[0])
          updateList["MPRT"] = "%s,%s" % (newPHost[1], newSHost[1])
        else:
          if newPHost:
            updateList["MURL"] = "%s,%s" % (newPHost[0], x.shost)
            updateList["MPRT"] = "%s,%s" % (newPHost[1], x.sport)
          if newSHost:
            updateList["MURL"] = "%s,%s" % (x.phost, newSHost[0])
            updateList["MPRT"] = "%s,%s" % (x.pport, newSHost[1])

        if newPUser and newSUser:
          updateList["USPA"] = "%s,%s" % (newPUser, newSUser)
        else:
          if newPUser:
            updateList["USPA"] = "%s,%s" % (newPUser, x.suser)
          if newSUser:
            updateList["USPA"] = "%s,%s" % (x.puser, newSUser)


        for item in updateList:
          try:
            x.form[item] = updateList[item]
          except (ValueError, TypeError):
            print "Somehow item %s doesn't exist" % item


        print "Updating..."
        try:
          result = x.uploadRestart()
        except blade.BladeError, err:
          print "[$s] ERROR: %s" % (x.address, err.msg)
          return False

        print "[%s] %s: %s" % (x.address, result.reason, result.content)


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print "CTRL-C"

