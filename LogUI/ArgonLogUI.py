from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import yaml
import os


# 弹出菜单
class TreePopMenu(Menu):
    def __init__(self):
        Menu.__init__(self, tearoff=0)
        self.path = StringVar()
        self.add_command(label="复制")
        self.add_separator()
        self.add_command(label="导出")


# 动态分配节点图片
def changephoto(status):
    if status == 'Fail':
        return fail_image
    elif status == 'Pass':
        return pass_image
    elif status == 'Info':
        return info_image
    elif status == 'Warning':
        return warning_image
    elif status == 'Error':
        return error_image
    elif status == 'Skip':
        return skip_image
    else:
        return None


# 导入图片
def importimage(name):
    cur_image = Image.open(name)
    cur_image = cur_image.resize((20, 20), Image.ANTIALIAS)
    return ImageTk.PhotoImage(cur_image)


if __name__ == '__main__':
    # 读取配置文件
    # casename = 'Standard Process Testing'
    # casename = 'test_skip_procedure'
    # casename = 'test_standard_procedure'
    casename = 'test_standard_fail'

    # 窗体设置
    window = Tk()
    window.title('Argon Log')
    # 窗口大小
    width, height = 600, 600
    # 窗口居中显示
    window.geometry('%dx%d+%d+%d' % (width, height, (window.winfo_screenwidth() - width) / 2, (window.winfo_screenheight() - height) / 2))
    window.resizable(0, 0)
    window.iconbitmap(r'1.ico')

    popmenu = TreePopMenu()

    frame = LabelFrame(window, height=500, width=500)
    frame.pack(fill=BOTH, expand=True)
    tree = ttk.Treeview(frame, show='tree')

    ysb = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    xsb = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
    tree.configure(yscroll=ysb.set, xscroll=xsb.set)

    tree.pack(fill=BOTH, expand=True)
    ysb.pack(fill=Y, side=RIGHT)
    xsb.pack(fill=X, side=BOTTOM)


    def rclfun(event):
        iid = tree.identify_row(event.y)
        tree.selection_set(iid)
        popmenu.post(event.x_root, event.y_root)


    tree.bind("<Button-3>", rclfun)

    # 图标集合
    pass_image = importimage(r'Pic/pass.png')
    fail_image = importimage(r'Pic/fail.png')
    send_image = importimage(r'Pic/send.png')
    sw_image = importimage(r'Pic/sw.png')
    recv_image = importimage(r'Pic/recv.png')
    case_image = importimage(r'Pic/case.png')
    info_image = importimage(r'Pic/info.png')
    warning_image = importimage(r'Pic/warning.png')
    error_image = importimage(r'Pic/error.png')
    skip_image = importimage(r'Pic/skip.png')

    for i ,yml in enumerate(os.listdir(r'../Log')):
        stream = open(r'../Log/' + yml, 'r')
        data = yaml.load(stream)
        stream.close()

        case = tree.insert('', i, yml[:-4], text=yml[:-4], image=case_image)
        tree.item(case, open=False)

        # 循环读入交易
        for x, trans in enumerate(data):
            photo = changephoto(trans['status'])
            cur_trans = tree.insert(case, x, str(i)+str(x)+trans['msg'], text=trans['msg'], image=photo)
            tree.item(cur_trans, open=True)

            # 循环读入模块
            for y, module in enumerate(trans['module']):
                photo = changephoto(module['status'])
                cur_module = tree.insert(cur_trans, y, str(i)+str(x)+str(y)+module['msg'], text=module['msg'], image=photo)
                tree.item(cur_module, open=True)

                # 循环读入比较
                for z, match in enumerate(module['list']):
                    photo = changephoto(match['status'])
                    cur_match = tree.insert(cur_module, z, str(i)+str(x)+str(y)+str(z)+match['msg'], text=match['msg'], image=photo)
                    tree.item(cur_match, open=False)
                    if len(match) == 8:
                        tree.insert(cur_match, 0, text=match['send'], image=send_image)
                        if match['a-SW'] != '':
                            tree.insert(cur_match, 1, text=match['a-SW'], image=sw_image)

                        def checksw(prtn, pSW):
                            if isinstance(pSW, list):
                                for sw_param in pSW:
                                    if sw_param == prtn:
                                        return True
                            elif isinstance(pSW, str):
                                if (pSW == prtn) | (pSW == ''):
                                    return True
                            else:
                                raise Exception('Wrong SW Type')
                            return False

                        if not checksw(match['a-SW'], match['r-SW']):
                            photo = changephoto('Fail')
                        else:
                            photo = changephoto('Pass')

                        if match['r-SW'] != '':
                            tree.insert(cur_match, 2, text=match['r-SW'], image=photo)

                        if match['a-recv'] != '':
                            tree.insert(cur_match, 3, text=match['a-recv'], image=recv_image)
                        # TODO
                        if (match['a-recv'] != '') & (match['r-recv'] != ''):
                            if match['a-recv'] != match['r-recv']:
                                photo = changephoto('Fail')
                            else:
                                photo = changephoto('Pass')
                            tree.insert(cur_match, 4, text=match['r-recv'], image=photo)
                    elif len(match) == 5:
                        tree.insert(cur_match, 0, text=match['a-value'], image=recv_image)
                        if match['a-value'] != match['r-value']:
                            photo = changephoto('Fail')
                        else:
                            photo = changephoto('Pass')
                        tree.insert(cur_match, 2, text=match['r-value'], image=photo)

    # 运行窗体
    window.mainloop()
