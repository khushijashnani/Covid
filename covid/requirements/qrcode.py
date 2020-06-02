import pyqrcode as qr

def send_qr(data,email):
    print("a")
    a = qr.create(data)
    print("b")
    fi = data +'.png'
    print(fi)
    a.png('covid\\requirements\\qrcodes\\'+fi,scale=7)
    return fi
