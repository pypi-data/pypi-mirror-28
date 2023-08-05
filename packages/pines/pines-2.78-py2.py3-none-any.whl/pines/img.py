


import base64, os


# data:image/png;base64
favicon = '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%3D'

eye = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAABgUExURUxpcQCj2wCPxQCa1QCZ1ACd2QCMwgCDuQCP0wCs3wBvoACOxwCGvACOxwCPxgCY0QCPzwCTzACTywCj1QCa2ACU1gCe2QCl3ACi2wCp3QCj5ACY4ACy6ACs6AC37ACt5OoTzCwAAAAUdFJOUwD7XPrR+0UE/f0WnCxwz6rquoflF5GMKAAAApRJREFUWMPtVtmCoyAQFCGKt0aNkUP+/y+nOQRijk12Z99SM5kM3V0F3ZxJ8sUXX/x35B5/RX7dfoddZum5ApzTrPxIQ8eVaUVwsTkUmFRp6Vzv0LNuFJtQhYeC5thlb0iAP2+I2iKyF9kUafLXEpBl3oybKIrVcMS2Cf0xjVW3R5B4XgtwpCOMfLV06BHqB5WEEVmJFXIZ06eDyJN6UALCDJTq6t1Td0o5cyHUUD9UAFuDxbpDjFlYSVDWMXLh5sEg8qQcRIFcDJJjaSqSJ+6rHKV3FmIojwp5kvViXXYozQ8x+t9yVN69ij47KjRXhZYgkFl+2rVtl1qFLAgsSF2b2/QruQQ+kp2h1K2SANXWptnJKGSRlS8EfA0SXSMstU67xhIZSGzbSxyD5OAUQLy94SNFjIfsViSJiSPqJky2Jk3DP100rub3guRZd5hKdHFAMtWWs7G4qMvltCs4/nUPP9nwzskaS2clveXqFYDPvNmFMzNHJNhPjJiZvo/UYyD/IkD0EAjDU4wTsykEM2Y2BXa6CcSWf6eAmS1iLGCLeIwj+zTcKmDW2mncrZjZaWwPYSTfF0IyMDxP7meGj1tIDBswt5Csc7JhmA3xUqzYvEP7KruUCWOcM0bsUq6glwBWJfFuSxo+Rd7ZbyZC/GaK/RM/nAl6O3Ma/P39du5DD5Tfb2d9oLCZ+oj2eKC0Xp/O7P5AsWlQTulMqf6j+4iPND0+64Gg5uG5qus88Jk6jYlW4VCtoOkcMx/qZye7rlofJDht7bHe6pHt9D59cbeYi8VKGHCuc+Z8bwP95cXirzYeNAJA6I9XW7hc+4MGsPu3Ltf4etcsi5l+cL3HD4zGPjCaDx8Yv/DE+Y1H1hdffPEhfgDKU1gnLBbrLAAAAABJRU5ErkJggg=='

favicon_raw = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x03\x00\x00\x00D\xa4\x8a\xc6\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x03\x00PLTE\x00\x00\x00\r(\x02\x0e)\x02\x10,\x02\x00\x00\x00\x00\x00\x00\x0c\x1a\x08\x7f\x7f\x7f\x00\x00\x00\x00\x00\x00SSS\x00\x00\x00\x02\x02\x02\x7f\x7f\x7f\x162\n\x02\x03\x02\x177\x0b,_\x16\x00\x00\x00\x00\x04\x00,`\x16\r\x1a\x08\x7f\x7f\x7f\r&\x02\x7f\x7f\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x164\n\x00\x00\x00\x174\n\x00\x00\x00\x178\x0b\x00\x00\x00\x176\n@@@)\\\x14+^\x16,b\x17ccc???\x0b\x15\x05\x0c\x17\x06\x12\x12\x12\x0c#\x02\r&\x02\x03\r\x03\x12#\n\x19\x19\x19""\x17\x00\x00\x00\x12*\t\x1dQ\t\x0e\x0e\x0e\x03\x03\x03\x02\x06\x01\x03\x03\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\'X\x13\x0b\x1b\x05"R\x0e\x0f\x0f\x0f\x162\n\x00\x00\x00\x10/\x03\x00\x00\x00\x07\x10\x04\x00\x00\x00\x00\x00\x00\x0f#\x07"S\x0e\x1a;\x0b\x00\x00\x00\x1a<\x0bU\x7fU(Y\x13\x08\x17\x03\x00\x00\x00\x08\x16\x03+]\x16\x00\x00\x00?\x81#\x00\x00\x00\x00\x00\x00\x08\x11\x03\x00\x00\x00D\x9b I\xa6"C\x99 I\xa7"J\xa9#J\xa8"G\xa1!F\xa0!D\x9a G\xa0!G\xa2!F\x9f E\x9d H\xa3!K\xab#H\xa4!M\xaf$\x01\x02\x00P\xb6%K\xac#B\x97\x1f=\x8b\x1c@\x94\x1cT\xc0\'L\xae$E\x9e X\xc8)I\xa5"J\xaa#L\xad#C\x97\x1fA\x96\x1dS\xbd\'O\xb5%?\x93\x1bK\xaa#L\xac#M\xb0#\x02\x04\x01\x03\x07\x01@\x91\x1eD\x9c\x1e=\x91\x1bD\x9e\x1f\x12*\x08D\x9c V\xc5(A\x94\x1e\x14-\t\x08\x13\x04Z\xcf*\r\x1e\x06A\x98\x1d@\x97\x1cF\x9e!>\x8d\x1cB\x99\x1e=\x8e\x1c:\x89\x1aC\x9b\x1e,f\x15C\x9a\x1f\x15/\tN\xb3$\x02\x05\x01T\xbf\'P\xb7%;\x87\x1bM\xb1$1p\x16R\xb6)3u\x18+c\x14S\xb8)B\x96\x1f$R\x11<\x8a\x1c:\x86\x1b\x162\n\x07\x10\x03W\xc6)?\x90\x1eY\xcb)\\\xd1+A\x95\x1fU\xc3(^\xd8,K\xa6&;\x8b\x1aG\x9d$M\xac\'?\x8f\x1dJ\xa9"O\xb0(8\x82\x1aR\xbc&*^\x13M\xb1%:\x83\x1a2r\x17>\x90\x1c5|\x185z\x19H\xa8!Q\xb8&M\xae$:\x85\x1bK\xac$W\xc7)\x0f#\x07Q\xb3(E\xa1\x1f\x04\x08\x02O\xb4%\x10$\x07R\xbb&\x1cA\rS\xbe\'\'Y\x12\x163\n\x04\x0b\x02\x0b\x1a\x05@\x93\x1d\r\x1d\x06U\xc2(\\\xd2+\'W\x12]\xd5,$T\x11<\x8c\x1a@\x91 A\x95\x1fJ\xa3%L\xa9\'K\xa5&E\x9b!Q\xa9-E\x9d!@\x93\x1fR\xbc\'-g\x15M\xad#6\x7f\x18O\xae\'D\xa0\x1fP\xb1(S\xb7)0m\x16\x19:\x0c-i\x15F\xa3 *`\x13J\xad"R\xb5(\\\xd3+b\xde-Q\xb9&P\xb3%1q\x17/k\x16X\xc7)^\xd5,\x186\x0b\x0f!\x07#Q\x11\x11\'\x08 I\x0f\n\x17\x05}\xb8;O\x00\x00\x00WtRNS\x00\xbf\xbf\xbf#\x7f\xb9\x04\x1d\x1b\x02!\x16\x06\xf1\x81\xf1\xf5\x07\x19\xf5\xb9\x10\xbe\rs}1\xf1i\xf1\'\xf0\x86\xf2\x06\xf5\xf5\xf5\t\x04\xb4\xb9\x0e\xb4\xbfM\x96\n\x16]\xec\xf5\x12\xa0\xc7\x9d.ZT\xf3\xd9\xf9\x10\xd8\xf6\xcd\xd4\xfdn|\xf9\xf1\xefz\xef\x06\xf4\x985\xd9\xf5d\xfdK\x92\x9e\x83\x12o\x03\x00\x00\x03$IDAT8\xcbc`\xa0\x02`\xe7\xc5%\xc3\x05\x96\xe1b0\xd4\xd7\x15gdd\x02\x02f0\x00\xb1\x98\x18\x19\xc5u\xf4\x18\x94A\xf2,&S7\xde[\xbf\xe9\xf9\xd6c\x0b\xe7\xbd\xfa\x08$\x16~|\xb9u\xd3\xdd\xf5w6N\xf2cPg\x90`pz\xb0\xb7\x7f\xd2\xc4=y\xe5\xe5y\x8d\x8dI\xfb\x1b\x9b\xcb\x81\xa0j\xcf\x86\r\xbb\x9a\x82C4\x18x\x85<\xaa\xfa#\xee\xc7\xa7G\xc6\x94\xe6\xa7\x9d\x9e}\xad"\xb6\xa22&\xb68\xa9/!*\xf7f\x98\x10\x03;\x8fo\xc2\xc4\x88\xc2\xc4\xb8\x98\x9a\x98\xb7)E\xe7:O~\xf9\x96\xfb5\xb681qj\xce\xcaK\x9a<\x0c\xec\xc2*S\x1b\n\xcb\xe2\xb2\x13#\xb2\x8e.o\xfb\xde\xb9\xfa\\\xf8\x929kJ##\x12ZoUiq2\xb0s\xaaNn/\xfc\x1a\x7fz\xf1\xa9\xb6\xac\xcb-\x8b/.\x08_\xbazngm\xe2\xf4\xd4\x885yl\x1c@\x05\x82\xcd\xed\xd1\xef\x97\xac:s\xaa\xed\xe4\x95\x8e\xf0\xfa\xf0\x86\xb5\xf9\xf3\xeb\x0b\xa6\xef\xc8\x8d|\xd4\x0bQp\xbc!\xfd|x\xf6\x8d\xee\xae\xac\x15k\xbb\xc3W^\x9fsu\xf7\x89\xedo\xc2g\xc7\xaf\xe9\x01+PkN\xa99\xfb\xeb\xe2\xb4\xbfG\xf2\xd7v\x9d\x0f\x9f\xb5\xeal\xd7\xfc\x0bg\xea\x92\xb3"\x13 &\x88\xbc[\xb2o\xef\xa1\xdf\xe1\x1d\xab\xf2W\\\xef\x08\xff\xfa\xf3\xc0\xba\xd7\xe1u\x0b\x96\xcc_\x1a\xd5#\nR\x10\xf8aq\xf8\x89\xf0\xe5\x17\xc2\xaf]\x9d\xb9nYx\xc5\x8fO\xfd32\x97\xcf\xa8\x0b\xef\x8e\xea\x05+P;^\x16\x91\x9c\x14\x9d\xdb\x19~\xa3kuG\xf8\xc1\xcf\xdb\xea\xc3\xa7d\xc7\xa7G\xa5@M\x10yQV\x1cY\xb0\xf3J\xeb\xff\xf0\x7f@\x13\xdav\x85g\xee^1}\xce\x96\xe2\xb8(\x88#E\x9a\xcb\x92\xd2c3\x0e\xe7\'u\x87\xffi\t_0#s_Q\xe9\xce\xea\xe8\xb8\xe4\x1c\xa87\x1b\x17%\xa5\xc6d\x9f\xcc\xc8/\xb9\x1c\x9e\x19\x9eY\xb7\xad(#\xab \r\xa8`\x114\xa0&\xb7\'\'FVgW\xd6\x9e-=\x1a\x9eY\xbf\xf4\x08H>6\xb5/\xa5\xbd\n\xac@uBCa_jtZvVu\xd1\xdc\xf0\xf0eE5\xb3\njb\x8a\xe3Z#n\x81\x15\x08\xabL\x988\x15\xe8\x8d\xc8\xd8\xd2\x92\x8a)\xe1\xe1\x1d\x07j\x0e\xc6D\xa7\'\xa6D\xe5\xacl\xd2\xe2`\xf0\xe1\xb1\xb9\xd4\x9f\x10\x11\x9f\x1a\x19\x9b\x11=\xf3Ix\xf8\xb4\xc71\x19%\xb1\xe9q\x85Qe\xfd759\x18\xd4\x85\x1c\x1e\x1eZ\xb9\xf9\xd1\xa2\xa8\x84\xf8\x84\xa7;\xc2\xc3[\xaaS\xe2S\x12r\xd6\xac\xdc<;gn(7\x03\x83\xbd\xac]\xde\x84\xe4\xb8\xc8\xd8\x92\xda-`\x13\xb6\xa7\xd5\xa6\x95D\xa7\xc7\xa7\xe4<\x0b\x08\xe2a`P\xb6\xe4\xb7\x95\xe3\x93\x91\x93\x13PP\xf2v\x0f\x0fw\xf1\x14P\x10\x10\x90\x93\xe1\xe336\xe7\xf7\xd7\x00\xa6{\x03ikI)VVV~/EY\xe7\xf0pGWE7V\x10\x90\x924\x92\x16\x82\xe4\x0fS\x0en\x16 \xe0\x96\xe7\xb12\xb3\xe0\x17\x96\x07\xf3X\xb89\xb4\xb9H\xcf\x86\xbcbb\x12\x0cT\x06\x00\xd9\xdcJ.\xbbbp\x06\x00\x00\x00\x00IEND\xaeB`\x82'


georgiatechlogo= "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"

camsyslogo = "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"

from .xhtml import Elem

georgiatechlogo_element = Elem('img', {
                'src': "data:image/png;base64,{}".format(georgiatechlogo),
                'style': 'float:right;max-height:40px;margin-top:0;margin-right:20px;margin-left:20px'
            })

camsyslogo_element = Elem('img', {
                'src': "data:image/png;base64,{}".format(camsyslogo),
                'style': 'float:right;max-height:44px;margin-top:0'
            })




_use_local_logo = False



def local_logo(filename=None):
	from .configure import cached, save
	cfg = cached()

	if filename is not None and os.path.exists(filename):
		png = base64.b64encode(open(filename, "rb").read())
		cfg['local_logo'] = png
		save(cfg)

	if 'local_logo' in cfg:
		return cfg['local_logo']
