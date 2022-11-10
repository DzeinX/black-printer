# не реализованно
def ItIsInt(*args):
    ans = []
    for arg in args:
        try:
            int(arg)
        except TypeError:
            ans.append(arg)
        except ValueError:
            ans.append(arg)
    if len(ans) == 0:
        return args
    else:
        return ans


if __name__ == "__main__":
    q = [5, 10, -4, 0.5, '5']
    if ItIsInt(5, 10, -4, 0.5, '5') == [5, 10, -4, 0.5, 5]:
        print('yes')
    else:
        print('no')

