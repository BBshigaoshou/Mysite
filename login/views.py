from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import WebUser, CityWeather
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import gzip


# 首页视图函数
def index(request):
    return render(request, 'index.html')


def downExcel(request):
    useExcel()
    file = open('static/excel/result_buu.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="result_buu.xls"'
    return response


def webCode(request):
    return render(request, 'webCode.html')


def webExcel(request):
    return render(request, 'webExcel.html')


def webwork(request):
    return render(request, 'webwork.html')


def excelwork(request):
    return render(request, 'excelwork.html')


def homework(request):
    return render(request, 'homework.html')


def game(request):
    return render(request, 'game.html')


def String_fun_four(request):
    return render(request, 'str_four.html')


# 登录函数
@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        userPassword = request.POST.get('password')
    try:
        user = WebUser.objects.get(username=username)
        if userPassword == user.password:
            return redirect('/index/')
        else:
            error_msg = '密码错误'
            return render(request, 'login.html', {'error_msg': error_msg})
    except Exception as e:
        print(e)
        error_msg = '用户名不存在'
        return render(request, 'login.html', {'error_msg': error_msg})


# 注册函数
@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('userName')
        userEmail = request.POST.get('userEmail')
        userPassword = request.POST.get('userPassword')
        userRePassword = request.POST.get('userRePassword')
        try:
            user = WebUser.objects.get(username=username)
            if user:
                msg = '用户名已存在'
                return render(request, 'registe.html', {'msg': msg})
        except Exception as e:
            print(e)

            if userPassword != userRePassword:
                error_msg = '密码不一致'
                return render(request, 'registe.html', {'error_msg': error_msg})
            else:
                new_user = WebUser()
                new_user.username = username
                new_user.password = userPassword
                new_user.email = userEmail
                new_user.save()
                return redirect('/login/')
    else:
        return render(request, 'registe.html')


# 字符串拼接加去除特殊字符
@csrf_exempt
def String_fun_one(request):
    if request.method == 'GET':
        return render(request, 'str_one.html')
    request.encoding = 'utf-8'
    result_one = ''
    if 'first_str_one' in request.POST or 'first_str_two' in request.POST:
        result_one = String_one(request)
    return render(request, 'str_one.html', {'result_one': '查询结果为：' + result_one})


@csrf_exempt
def String_fun_two(request):
    if request.method == 'GET':
        return render(request, 'str_two.html')
    result_two = ''
    if 'second_str' in request.POST:
        result_two = String_two(request)
    return render(request, 'str_two.html', {'result_two': '输入结果为： ' + result_two})


@csrf_exempt
def String_fun_three(request):
    if request.method == 'GET':
        return render(request, 'str_three.html')
    request.encoding = 'utf-8'
    result_search = ()
    if 'my_birth' in request.POST:
        birthTime = request.POST.get('my_birth')
        if len(birthTime) == 8:
            year = int(birthTime[0:4])
            month = int(birthTime[4:6])
            day = int(birthTime[-2:])
            if 0 <= month <= 12 and 0 <= day <= 31:
                result_search = String_search(request)
    if result_search != ():
        return render(request, 'str_three.html', {'result_shengxiao': result_search[1],
                                                  'result_date': '星座时间段： ' + result_search[0]['date'],
                                                  'result_Constellation': '星座： ' + result_search[0]['Constellation'],
                                                  'result_character': '星座运势： ' + result_search[0]['character']})
    else:
        return render(request, 'str_three.html', {'result_shengxiao': '输入格式错误'})


@csrf_exempt
def String_one(request):
    if request.method == 'POST':
        str_one = str(request.POST.get('first_str_one'))
        str_two = str(request.POST.get('first_str_two'))
        if str_one == '' or str_one == '':
            return ''
        else:
            new_str = fuc_str_one(str_one, str_two)
            return new_str
    else:
        return ''


@csrf_exempt
def String_two(request):
    if request.method == 'POST':
        str_two = request.POST.get('second_str')
        if str_two == '':
            return ''
        else:
            new_str = fuc_str_two(str_two)
            return new_str
    else:
        return ''


# 查询生日数据
@csrf_exempt
def String_search(request):
    if request.method == 'POST':
        birthTime = request.POST.get('my_birth')
        if birthTime == '':
            return None
        else:
            search_info = fun_search(birthTime)
        return search_info
    else:
        return None


# 查询城市天气
@csrf_exempt
def find_weather(request):
    if request.method == 'GET':
        return render(request, 'weather.html')
    elif request.method == 'POST':
        city = request.POST.get('city')
        weather_dict = spider_weather(city)
        if weather_dict.get('desc') == 'invilad-citykey':
            msg = '城市不存在'
            return render(request, 'weather.html', {'msg': msg})
        # 把过去的数据删除
        before_info = CityWeather.objects.all()
        before_info.delete()
        # 插入昨天的天气
        yes_city = CityWeather()
        yes_city.cityname = city
        yes_city.date = weather_dict['data']['yesterday']['date']
        yes_city.high = weather_dict['data']['yesterday']['high']
        yes_city.low = weather_dict['data']['yesterday']['low']
        yes_city.fl = weather_dict['data']['yesterday']['fl'][-5:-3]
        yes_city.fx = weather_dict['data']['yesterday']['fx']
        yes_city.type = weather_dict['data']['yesterday']['type']
        yes_city.save()
        # 插入预测的天气
        for each in weather_dict['data']['forecast']:
            new_city = CityWeather()
            new_city.cityname = city
            new_city.date = each['date']
            new_city.high = each['high']
            new_city.low = each['low']
            new_city.fl = each['fengli'][-5:-3]
            new_city.fx = each['fengxiang']
            new_city.type = each['type']
            new_city.save()
        # 返回到所有数据库中天气数据
        weatherlist = CityWeather.objects.all()
        return render(request, 'weather.html', {'weatherlist': weatherlist,
                                                'inputmsg': '天气情况为：'})
    else:
        return render(request, 'weather.html')


# 将两个字符串拼接
def fuc_str_one(s1, s2):
    newStr = ""
    while len(s1) != 0 and len(s2) != 0:
        newStr += s1[0]
        newStr += s2[0]
        s1 = s1[1:]
        s2 = s2[1:]
    newStr += (s1 + s2)
    return newStr


# 将字符串除去特殊字符
def fuc_str_two(oldStr):
    if oldStr.isalnum():
        return oldStr
    else:
        newStr = ""
        for ch in iter(oldStr):
            if 47 < ord(ch) < 58 or 64 < ord(ch) < 91 or 96 < ord(ch) < 123:
                newStr += ch
        return newStr


# 搜索对应时间的生肖星座信息
def fun_search(birth):
    # 通过输入生日判断对应的星座编号
    def birth_to_flag(birtime):
        if birtime <= 119 or 1222 <= birtime:
            return 1
        elif 120 <= birtime <= 218:
            return 2
        elif 219 <= birtime <= 320:
            return 3
        elif 321 <= birtime <= 419:
            return 4
        elif 420 <= birtime <= 520:
            return 5
        elif 521 <= birtime <= 621:
            return 6
        elif 622 <= birtime <= 722:
            return 7
        elif 723 <= birtime <= 822:
            return 8
        elif 823 <= birtime <= 922:
            return 9
        elif 923 <= birtime <= 1023:
            return 10
        elif 1024 <= birtime <= 1122:
            return 11
        elif 1123 <= birtime <= 1221:
            return 12

    # 通过星座编号获取到星座对应的信息
    def flag_to_XingZuo(flag):
        values = {
            1: {'Constellation': "摩羯座", 'date': "12月22日-1月19日",
                'character': "摩羯座是十二星座中最有耐心，行事最小心、也是最善良的星座.他们做事脚踏实地,也比较固执，不达目的是不会放手的。他们的忍耐力也是出奇的强大，同时也非常勤奋.他们心中总是背负着很多的责任感,但往往又很没有安全感,不会完全地相信别人。"},
            2: {'Constellation': "水瓶座", 'date': "1月20日-2月18日",
                'character': "水瓶座的人很聪明，他们最大的特点是创新，追求独一无二的生活，个人主义色彩很浓重的星座。他们对人友善又注重隐私。水瓶座绝对算得上是“友谊之星”，他喜欢结交每一类朋友，但是却很难与他们交心，那需要很长的时间。他们对自己的家人就显得冷淡和疏远很多了。"},
            3: {'Constellation': "双鱼座", 'date': "2月19日-3月20日",
                'character': "双鱼座是十二宫最后一个星座，他集合了所有星座的优缺点于一身，同时受水象星座的情绪化影响，使他们原来复杂的性格又添加了更复杂的一笔。双鱼座的人最大的优点是有一颗善良的心，他们愿意帮助别人，甚至是牺牲自己。"},
            4: {'Constellation': "白羊座", 'date': "3月21日-4月19日",
                'character': "白羊座的人热情冲动、爱冒险、慷慨，天不怕地不怕。而且一旦下定决心，不到黄河心不死，排除万难也要达到目的。大部分属于白羊座的人的脾气都很差，不过只是炮仗颈，绝对不会放在心上的。"},
            5: {'Constellation': "金牛座", 'date': "4月20日-5月20日",
                'character': "金牛座是很保守的星座，喜欢稳定，不爱变动。在性格上则比较慢热，对工作、生活、环境都需要比较长的适应期。金牛座又往往是财富的象征，他们在投资理财方面常常有很独到的见解。金牛座的男人往往有大男人的倾向，而金牛女生则喜欢打扮自己，谁让金牛的守护神是维纳斯呢？"},
            6: {'Constellation': "双子座", 'date': "5月21日-6月21日",
                'character': "双子座的人往往喜好新鲜事物，他们有着小聪明，但做事常常不太专一。与双子座的人聊天也许会让你觉得很兴奋，因为他们脑子中那些新鲜的、稀奇古怪的东西会让人充满好奇。也许是对新鲜事物的追求和好奇，会让人觉得他们很花心，其实不然，他们仅仅是喜欢新鲜而已。"},
            7: {'Constellation': "巨蟹座", 'date': "6月22日-7月22日",
                'character': "巨蟹座的人往往充满了爱心，他们将母性的本质发挥到了极限。对他们来说，最重要的东西是家庭。他们往往就像蟹一样，在充满坚硬的外壳下面是柔软的内心。巨蟹座是最执着的星座，他们对朋友、对家人非常忠实，做事也会一直坚持到底"},
            8: {'Constellation': "狮子座", 'date': "7月23日-8月22日",
                'character': "狮子座的人开朗、豪爽。这些是他们性格上最大的特色。对人真诚、自信而从容不迫，狮子座的人擅长把自己的优势放大，有号召力、气场强，是十二星座中颇具领导才能的一个星座，他们有很强的领地意识，自己人不容他人冒犯"},
            9: {'Constellation': "处女座", 'date': "8月23日-9月22日",
                'character': "处女座追求完美，吹毛求疵是他们的特性。多数的处女座都很谦虚，但也因此给自己造成很大的压力。处女座的人不喜欢闲着，对别人常常乐于服务。缺乏自信的处女座有时候组织能力较差，需要家人与朋友们的鼓励去推动他们。"},
            10: {'Constellation': "天秤座", 'date': "9月23日-10月23日",
                 'character': "天秤座常常追求和平和谐的感觉，他们善于交谈，沟通能力极强是他们最大的优点。但他们最大的缺点，往往是犹豫不决。天秤座的人容易将自己的想法加诸到别人身上，天秤座的人要小心这点。天秤座女生常常希望他们的伴侣会时刻陪伴着她。"},
            11: {'Constellation': "天蝎座", 'date': "10月24日-11月22日",
                 'character': "天蝎座的人精力旺盛、热情、善妒，占有欲极强。他们想要每天过得非常充实，如果失去了目标，他们很难认真地投入精力。天蝎是记仇的，会不顾一切地打击仇人。他们的一个成功优点，就是他们一旦定了目标，就会不达目的誓不罢休。"},
            12: {'Constellation': "射手座", 'date': "11月23日-12月21日",
                 'character': "射手座的人就像那只在弦上的箭一样，他们主动出击。为人乐观、诚实、热情、喜欢挑战。射手是十二星座中的冒险家，热爱旅行、喜欢赌博。意志力薄弱是射手座天生的弱点，如果沉迷赌博与游戏，后果不堪设想。"},
        }
        return values.get(flag)

    # 通过出生年判断生肖
    def shengxiao(year):
        if year % 12 == 0:
            return '生肖属猴'
        elif year % 12 == 1:
            return '生肖属鸡'
        elif year % 12 == 2:
            return '生肖属狗'
        elif year % 12 == 3:
            return '生肖属猪'
        elif year % 12 == 4:
            return '生肖属鼠'
        elif year % 12 == 5:
            return '生肖属牛'
        elif year % 12 == 6:
            return '生肖属虎'
        elif year % 12 == 7:
            return '生肖属兔'
        elif year % 12 == 8:
            return '生肖属龙'
        elif year % 12 == 9:
            return '生肖属蛇'
        elif year % 12 == 10:
            return '生肖属马'
        elif year % 12 == 11:
            return '生肖属羊'

    year = int(birth[0:4])  # 年份取字符串前四位改为int类型
    month = int(birth[4:6])  # 生日取字符串后四位改为int类型
    day = int(birth[-2:])
    # 如果输入字符串是8位年月日并且满足格式，退出循环
    if len(birth) == 8 and 0 <= month <= 12 and 0 <= day <= 31:
        # 用月份乘100再加上日期，得到生日方便判断星座
        birtime = month * 100 + day
        flag = birth_to_flag(birtime)
        infoDict = flag_to_XingZuo(flag)
        shengxiao = shengxiao(year)
        return infoDict, shengxiao
    else:
        return None


# 爬取天气数据返回字典
def spider_weather(city):
    urllib.parse.quote(city)
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + urllib.parse.quote(city)
    weather_data = urllib.request.urlopen(url).read()
    weather_data = gzip.decompress(weather_data).decode('utf-8')
    weather_dict = eval(weather_data)
    return weather_dict


# 导师随机分配
def useExcel():
    import random
    import xlrd
    from xlutils.copy import copy

    # 打开文件
    teacherData = xlrd.open_workbook('static/excel/teacher_buu.xlsx')
    studentData = xlrd.open_workbook('static/excel/student_buu.xlsx')

    # 2. 获取sheet内容
    # 按索引号获取sheet页的内容
    teacher_content = teacherData.sheet_by_index(0)
    student_content = studentData.sheet_by_index(0)

    # 3. 获取整行和整列的值（数组）
    teacher_rows = teacher_content.nrows
    teacher_name = teacher_content.col_values(0)  # 获取第四行内容
    teacher_num = teacher_content.col_values(1)  # 获取第三列内容
    # print(teacher_name)

    student_rows = student_content.nrows  # 37
    student_id = student_content.col_values(0)  # 获取第一列内容
    student_name = student_content.col_values(1)  # 获取第二列内容
    student_gender = student_content.col_values(2)  # 获取第三列内容
    # print(student_name)

    # 生成一个随机数组，将1-36打乱顺序放入数组，用于之后分配老师
    random_list = random.sample(range(1, student_rows), student_rows - 1)
    # sample(x,y)函数的作用是从序列x中，随机选择y个不重复的元素, 表示从[A,B)间随机生成N个数，结果以列表返回

    # 打开result表格，准备进行填充
    old_result = xlrd.open_workbook("static/excel/result_buu.xlsx")  # 先打开已存在的表
    new_result = copy(old_result)  # 复制
    new_sheet = new_result.get_sheet(0)  # 取其中的sheet页

    # 对老师根据对应学生数进行排号
    teacher1 = teacher_num[1]
    teacher2 = teacher1 + teacher_num[2]
    teacher3 = teacher2 + teacher_num[3]
    teacher4 = teacher3 + teacher_num[4]
    teacher5 = teacher4 + teacher_num[5]
    teacher6 = teacher5 + teacher_num[6]
    teacher7 = teacher6 + teacher_num[7]

    # for循环从1开始，因为下标为0的位置为"学生学号	学生姓名	学生类型"
    # 第一个老师负责随机数组中第1-6个学生，第二个老师负责7-10个学生...
    for i in range(1, student_rows):
        if i <= teacher1:
            teacher = teacher_name[1]
        elif teacher1 < i <= teacher2:
            teacher = teacher_name[2]
        elif teacher2 < i <= teacher3:
            teacher = teacher_name[3]
        elif teacher3 < i <= teacher4:
            teacher = teacher_name[4]
        elif teacher4 < i <= teacher5:
            teacher = teacher_name[5]
        elif teacher5 < i <= teacher6:
            teacher = teacher_name[6]
        elif teacher6 < i <= teacher7:
            teacher = teacher_name[7]
        new_sheet.write(i, 0, student_name[random_list[i - 1]])
        new_sheet.write(i, 1, student_id[random_list[i - 1]])
        new_sheet.write(i, 2, student_gender[random_list[i - 1]])
        new_sheet.write(i, 3, teacher)

    new_result.save("static/excel/result_buu.xls")  # 保存至result路径,为xls格式保存
