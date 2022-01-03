from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.views.generic.edit import UpdateView
from .forms import LoginForm, CreateUserForm, ProfileUpdateForm, ResetForm,VideoCreate,UserUpdateForm,CoupenCodeForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from order_app.models import Order, OrderItem,CouponCode
from course_app.models import Course,Video
from django.http import Http404, HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView ,TemplateView
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import (TeacherMixin, CourseValidMixin, CourseFieldMixin, BlogCreateFieldMixin, BlogCreateValidMixin,TeacherBlogUpadteMixin,TeacherCourseUpadteMixin,VideoUpdateMixin)
from blog_app.models import Blog
from django.contrib import messages
from cart_app.models import Cart,CartItem
from django.utils import timezone

# register view
class Register(CreateView):
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy('account:login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        messages.success(self.request,'ثبت نام با موفقیت انجام شد. وارد شوید')
        return super().form_valid(form)

    def form_invalid(self, form):
        # messages.error(self.request, 'یه مشکلی هست ، ببین ارور چی میگه ! ( اعتبار سنجی یادت نره )', 'danger')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        return super().dispatch(request, *args, **kwargs)


# login view
class Login(LoginView):
    redirect_authenticated_user = reverse_lazy('course:course_list')
    form_class = LoginForm

    def get_success_url(self):
        user = self.request.user
        try:
            if self.request.GET.get('next'):
                return resolve_url(f"http://127.0.0.1:8000{self.request.GET.get('next')}")
                # todo : set site url
            elif user.is_superuser:
                return reverse_lazy('account:profile')
            elif user.is_teacher:
                return reverse_lazy('account:profile')
            else:
                return reverse_lazy('account:profile')
        except:
            return reverse_lazy('account:profile')


# logout view
@login_required()
def logout_view(request):
    logout(request)
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    else:
        return redirect('/courses')


# password change view
class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:profile')

    def form_valid(self,form):
        messages.success(self.request,'رمز عبور شما با موفقیت تغییر کرد')
        return super().form_valid(form)


# password reset view
class PasswordReset(PasswordResetView):
    success_url = reverse_lazy('account:login')
    form_class = ResetForm

    def form_valid(self, form):
        messages.success(self.request,'لینک بازیابی رمز عبور به ایمیل شما ارسال شد')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        return super().dispatch(request, *args, **kwargs)


# password reset confirm view
class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        messages.success(self.request,'بازیابی رمز عبور با موفقیت انجام شد. وارد شوید')
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        return super().dispatch(request, *args, **kwargs)


# add course to order view
@login_required()
def add_course_to_cart(request, pk, *args, **kwargs):
    user_courses = request.user.student_courses.get_publish_course()
    cart = Cart.objects.get(user_id=request.user.id)
    if not cart or cart is None:
        Cart.objects.create(user_id=request.user.id)
    course_id = pk
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise Http404()
    if course in user_courses:
        return redirect('account:my_courses')
    if course is None or not course.status:
        raise Http404()
    item = cart.items.filter(course_id=course_id).first()
    if item in cart.items.all():
        return redirect('account:cart')
    else:
        if course.discount and 0 < course.discount <= 100 and course.price > 0:
            discount = course.discount
        else:
            discount = None
        cart.items.create(course_id=course_id,price=course.price,discount=discount)
    return redirect('account:cart')

# @login_required()
# def add_course_to_order(request, *args, **kwargs):
#     user_courses = request.user.student_courses.get_publish_course()
#     order = Order.objects.get(user_id=request.user.id, is_paid=False)
#     if order is None:
#         Order.objects.create(user_id=request.user.id, is_paid=False)
#     course_id = kwargs['pk']
#     course = Course.objects.get(id=course_id)
#     if course in user_courses:
#         return redirect('account:my_courses')
#     if course is None or not course.status:
#         raise Http404()
#     item = order.items.filter(course_id=course_id).first()
#     if item in order.items.all():
#         return redirect('account:cart')
#     else:
#         if course.discount and 0 < course.discount <= 100 and course.price > 0:
#             discount = course.discount
#         else:
#             discount = None
#         order.items.create(course_id=course_id, price=course.price, discount=discount)
#     return redirect('account:cart')


# delete course from order view
@login_required()
def delete_course_from_cart(request, pk, *args, **kwargs):
    item_id = pk
    if item_id:
        item = get_object_or_404(CartItem, pk=item_id)
        if item is not None:
            item.delete()
            return redirect('account:cart')
    raise Http404()


class ProfileUpdate(LoginRequiredMixin,TemplateView):
    user_form = UserUpdateForm
    profile_form = ProfileUpdateForm
    template_name = 'account/profile.html'

    def post(self,request):
        post_data = request.POST or None
        file_data = request.FILES or None       

        user_form = UserUpdateForm(post_data,instance=request.user)
        profile_form = ProfileUpdateForm(post_data,file_data,instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'عملیات با موفقیت انجام شد')
            return HttpResponseRedirect(reverse_lazy('account:profile'))
      
        context = {
            'user_form' : user_form,
            'profile_form' : profile_form,
        }

        return render(request,'account/profile.html',context)

    def get(self,request,*args, **kwargs):
        return self.post(request,*args, **kwargs)


# cart view
class CartView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        cart = Cart.objects.get(user_id=self.request.user.id)
        items = cart.items.all()
        return items

    template_name = 'account/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user_id=self.request.user.id)
        cart.coupon_code = None
        cart.save()
        context['cart'] = cart
        return context

# apply coupon code
@login_required()
def apply_coupon_code(request):
    if request.method == 'POST':
        form = CoupenCodeForm(request.POST)
        if form.is_valid():
            time = timezone.now()
            code = form.cleaned_data['code']
            try:
                coupon = CouponCode.objects.get(code__exact=code,start__lte=time,end__gte=time,status=True)
                cart = Cart.objects.get(user=request.user)
                cart.coupon_code = coupon
                cart.save()
                messages.success(request,'کد تخفیف با موفقیت اعمال شد.')
                return redirect('account:checkout')
            except CouponCode.DoesNotExist:
                messages.error(request,'کد تخفیف نامعتبر است.')
    return redirect('account:checkout')

# remove coupon code from cart
@login_required()
def remove_coupon_code(request):
    cart = Cart.objects.get(user=request.user)
    if cart.coupon_code:
        print(cart.coupon_code)
        cart.coupon_code = None
        cart.save()
        messages.success(request,'کد تخفیف با موفقیت حذف شد')
        return redirect('account:checkout')
    else:
        raise Http404()
        
# checkout view
@login_required()
def checkout(request):
    cart = Cart.objects.get(user_id=request.user.id)

    if cart.coupon_code:
        time = timezone.now()
        try :
            coupon = CouponCode.objects.get(code__exact=cart.coupon_code.code,start__lte=time,end__gte=time,status=True)
        except:
            cart.coupon_code = None
            cart.save()
            messages.error(request,'کد تخفیف منقضی شده است.')

    items = cart.items.all()
    if items.count() < 1:
        raise Http404()
        
    coupon_form = CoupenCodeForm(request.POST)
    context = {
        'cart':cart,    
        'items':items,
        'coupon_form':coupon_form,    
    }
    return render(request,'account/checkout.html',context)

# my courses view
class MyCourses(LoginRequiredMixin, ListView):
    def get_queryset(self):
        user = self.request.user
        courses = user.student_courses.get_publish_course().order_by('-course_app_course_student.id')
        return courses

    template_name = 'account/my-courses.html'


# add course view
class CourseAdd(LoginRequiredMixin, CourseValidMixin, CourseFieldMixin, TeacherMixin, CreateView):
    model = Course
    template_name = 'account/course-add.html'
    success_url = reverse_lazy('account:teacher_courses')

    def form_valid(self,form):
        messages.success(self.request,'درخواست شما با موفقیت ثبت شد')
        return super().form_valid(form)
    

# update course view    
class CourseUpdate(LoginRequiredMixin,TeacherMixin,TeacherCourseUpadteMixin,CourseFieldMixin,UpdateView):
    model = Course
    template_name = 'account/course-update.html'
    success_url = reverse_lazy('account:teacher_courses')


# teacher videos view
class VideoList(LoginRequiredMixin,TeacherMixin,ListView):
    
    def get_queryset(self):
        user = self.request.user
        videos = Video.objects.filter(course__teacher=user)
        return videos

    template_name = 'account/video-list.html'


# add video view
class VideoAdd(LoginRequiredMixin,TeacherMixin,CreateView):
    model = Video
    form_class = VideoCreate
    template_name = 'account/video-add.html'
    success_url = reverse_lazy('account:teacher_courses')

    def form_valid(self,form):
        messages.success(self.request,'درخواست شما با موفقیت ثبت شد')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(VideoAdd, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class VideoUpdate(LoginRequiredMixin,TeacherMixin,VideoUpdateMixin,UpdateView):
    model = Video
    form_class = VideoCreate
    template_name = 'account/video-update.html'
    success_url = reverse_lazy('account:teacher_videos')

    def form_valid(self,form):
        messages.success(self.request,'درخواست شما با موفقیت ثبت شد')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(VideoUpdate, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs    


# teacher courses course view
class TeacherCourses(LoginRequiredMixin, TeacherMixin, ListView):
    def get_queryset(self):
        user = self.request.user
        # courses = Course.objects.filter(teacher=user)
        courses = user.teacher_courses.all()
        return courses

    template_name = 'account/teacher-courses.html'


# my comments view
class MyComment(LoginRequiredMixin, ListView):
    def get_queryset(self):
        user = self.request.user
        comments = user.comments.all()
        return comments

    template_name = 'account/my-comment.html'


# teacher blogs view
class TeacherBlogs(LoginRequiredMixin, TeacherMixin, ListView):
    def get_queryset(self):
        user = self.request.user
        blogs = user.blogs.all()
        return blogs

    template_name = 'account/teacher-blogs.html'


# add blog view
class BlogCreate(LoginRequiredMixin, TeacherMixin, BlogCreateFieldMixin, BlogCreateValidMixin, CreateView):
    model = Blog
    success_url = reverse_lazy('account:teacher_blogs')
    template_name = 'account/blog-create.html'

    def form_valid(self,form):
        messages.success(self.request,'درخواست شما با موفقیت ثبت شد')
        return super().form_valid(form)
    

# update blog view    
class BlogUpdate(LoginRequiredMixin,TeacherMixin,TeacherBlogUpadteMixin,BlogCreateFieldMixin,UpdateView):
    model = Blog
    template_name = 'account/blog-update.html'
    success_url = reverse_lazy('account:teacher_blogs')


# paymant list view
class PaymentList(LoginRequiredMixin, ListView):
    def get_queryset(self):
        order = Order.objects.filter(user_id=self.request.user.id, is_paid=True)
        return order

    template_name = 'account/payment-list.html'


# detail view
class PaymentDetail(LoginRequiredMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        order = get_object_or_404(Order.objects.filter(user_id=self.request.user.id, is_paid=True),
                                  pk=pk)
        return order

    template_name = 'account/payment-detail.html'

