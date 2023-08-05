import xy_youtuyun
appid = '10114485'
secret_id = 'AKIDYtynLcYPu98rJVP6VdV7TYNyJOCkP6wW'
secret_key = 'SeZEcniMjqgIejXUDhvwhCRRAdqnUu4x'
userid = '382771946'
end_point = xy_youtuyun.conf.API_YOUTU_END_POINT

def facemix(filename='', model_id=0, return_type=0):
    if not filename:
        return -1
    youtu = xy_youtuyun.YouTu(appid, secret_id, secret_key, userid, end_point)
    facemix = youtu.FaceMix(filename,model_id,return_type)
    return facemix

def main():
    res = facemix('1.jpg')
    print(res)

if __name__ == '__main__':
    main()
