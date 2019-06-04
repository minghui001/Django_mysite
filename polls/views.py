from django.shortcuts import render,get_object_or_404
from .models import Question,Choice
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

# 首页，显示投票列表
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

#一个路由测试页面
def hello(request):
    return HttpResponse('hello worlde!')

# 投票详情，路由传递一个数字过来，在这里判断数字（问题的id）是否存在，并作出动作
# get_object_or_404会读取数据库Question，查找id，正确则返回object，错误则返回404页
# 之后的返回代码就不会被执行了，例如：return HttpResponse('this is test')，实际测试只返回404
# 页面中有提交的post，请求页面为id+vote，post内容为choice +安全码（防止跨站）
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # return HttpResponse('this is test')
    return render(request, 'polls/detail.html', {'question': question})

#投票结果，路由为一个数字+results，其中数字为问题的id
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# 投票，路由为id+vote，
# 提交的post choice=id
# 获取id后，投票结果+1，结果需要保存，
# 这里没有页面，只是一个处理数据的过程
# 如果没有选择就提交，则重新返回投票页，并增加一个提示
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 成功处理POST数据后，始终返回HttpResponseRedirect（Http响应重定向）。如果用户点击后退按钮，这将防止数据被发布两次。
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
