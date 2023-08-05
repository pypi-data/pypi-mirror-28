'''这个函数的作用是列表（包含N个嵌套）'''



#递归函数
def print_dg(the_list,indent=False,level=0,fh=sys.stdout):
#sys.stdout如果没有指定文件对象则会写至屏幕
  for ea_it in the_list:
    if isinstance(ea_it,list):
        print_dg(ea_it,indent,level+1,fh)
    else:
      if indent:
              for ta_st in range(level):
                print("\t",end='',file=fh)
      print(ea_it,file=fh)
#结束


