def ItIsInt(arg, ans) -> bool:
    if isinstance(arg, list):
        lt = []
        for ell_lt in arg:
            if isinstance(ell_lt, int):
                lt.append(int(ell_lt))
            else:
                if isinstance(ell_lt, float):
                    lt.append("err_val")
                    ans.append(lt)
                    return True
                else:
                    try:
                        if ell_lt == "True":
                            lt.append(1)
                        elif ell_lt == "False":
                            lt.append(0)
                        else:
                            lt.append(int(ell_lt))
                    except TypeError:
                        lt.append("err_val")
                        ans.append(lt)
                        return True
                    except ValueError:
                        lt.append("err_val")
                        ans.append(lt)
                        return True
        ans.append(lt)
    else:
        if isinstance(arg, int):
            ans.append(int(arg))
        else:
            if isinstance(arg, float):
                ans.append("err_val")
                return True
            else:
                try:
                    if arg == "True":
                        ans.append(1)
                    elif arg == "False":
                        ans.append(0)
                    else:
                        ans.append(int(arg))
                except TypeError:
                    ans.append("err_val")
                    return True
                except ValueError:
                    ans.append("err_val")
                    return True


def ItIsStr(arg, ans):
    if isinstance(arg, list):
        lt = []
        for ell_lt in arg:
            lt.append(str(ell_lt))
        ans.append(lt)
    else:
        ans.append(str(arg))


def ItIsFloat(arg, ans) -> bool:
    if isinstance(arg, list):
        lt = []
        for ell_lt in arg:
            if not isinstance(ell_lt, str):
                lt.append(float(ell_lt))
            else:
                try:
                    if ell_lt == "True":
                        lt.append(float(True))
                    elif ell_lt == "False":
                        lt.append(float(False))
                    else:
                        lt.append(float(ell_lt))
                except TypeError:
                    lt.append("err_val")
                    ans.append(lt)
                    return True
                except ValueError:
                    lt.append("err_val")
                    ans.append(lt)
                    return True
        ans.append(lt)
    else:
        if not isinstance(arg, str):
            ans.append(float(arg))
        else:
            try:
                if arg == "True":
                    ans.append(float(True))
                elif arg == "False":
                    ans.append(float(False))
                else:
                    ans.append(float(arg))
            except TypeError:
                ans.append("err_val")
                return True
            except ValueError:
                ans.append("err_val")
                return True


def ItIsBool(arg, ans) -> bool:
    if isinstance(arg, list):
        lt = []
        for ell_lt in arg:
            if not isinstance(ell_lt, str):
                lt.append(bool(ell_lt))
            else:
                try:
                    lt.append(bool(float(ell_lt)))
                except TypeError:
                    lt.append("err_val")
                    return True
                except ValueError:
                    lt.append("err_val")
                    return True
        ans.append(lt)
    else:
        if not isinstance(arg, str):
            ans.append(bool(arg))
        else:
            try:
                ans.append(bool(float(arg)))
            except TypeError:
                ans.append("err_val")
                return True
            except ValueError:
                ans.append("err_val")
                return True


def TypeVar(*args, var_type) -> [list, bool] or [str, bool]:
    ans = []

    if var_type == "int":
        for arg in args:
            if ItIsInt(arg, ans):
                return [ans, False]

    elif var_type == "str":
        for arg in args:
            if ItIsStr(arg, ans):
                return [ans, False]

    elif var_type == "float":
        for arg in args:
            if ItIsFloat(arg, ans):
                return [ans, False]

    elif var_type == "bool":
        for arg in args:
            if ItIsBool(arg, ans):
                return [ans, False]

    else:
        return ['Incorrect var_type', False]
    return [ans, True]


'''
if __name__ == "__main__":
    ans = []
    answer = TypeVar([True, 10, -4, 'True'], 9, '-2', 'False', var_type='int')

    if answer[1]:
        print(answer[0])
    else:
        if isinstance(answer[0], str):
            print(answer[0])
        else:
            print('Incorrect value')
'''
