/**
 * Created by hongpeng on 2017/3/8.
 */

function selectAll(){
    $(':checkbox').prop('checked',true)
}

function cancelAll(){
    $(':checkbox').prop('checked',false)
}
function reverseAll() {
    $(':checkbox').each(function () {
        var v = $(this).prop('checked')?false:true;
        $(this).prop('checked',v)
    })
}

function add_host() {
    $('.add_host,.background').removeClass('hide');
    $('.add_host input[type="text"]').val('');//清除数据
}
function show() {
    $('.add_host,.background').addClass('hide')
}

$('.delete').click(function () {
    $(this).parent().parent().remove();
})
$('.tl').click(function () {
    $(this).next().toggle(200);
//            $(this).next().removeClass('hide');
    $(this).parent().siblings().find('.content').addClass('hide');
//            console.log(1);
})

$('.edit').click(function () {
    $('.add_host,.background').removeClass('hide');
    var tds = $(this).parent().siblings();//获取所有的td
    tds.each(function () {
        var target = $(this).attr('target');//获取属性#hostname #ip #port
        var v = $(this).text();//获取值
        $(target).val(v);//赋值
        })
//            Change(this)
})
//

//            增加
$('.sure').click(function () {
    $('.add_host,.background').addClass('hide');
    var tr = document.createElement('tr');
    v1 = '<td><input type="checkbox"/></td>';
    $(tr).append(v1);
    var inputs = $('.info').children(':text');
    inputs.each(function () {
        var td_v = $(this).val();
        var td = document.createElement('td');
        td.innerHTML=td_v;
        $(tr).append(td);
    });
    v2 = '<td><input type="button"value="删除" /><br><input class="edit" type="button"value="编辑"/></td>';
    v2 = '<td><a>删除</a><a>编辑</a></td>';
    $(tr).append(v2);
    $('#tb').append(tr);

})
$('.praise').click(function () {
    AddFavor(this);
})
function AddFavor(self){
    var tag = document.createElement('span');
    $(tag).text('+1');
    $(tag).css('position','absolute');
    $(self).append(tag);
    var fontSize = 12;
    var top = -1;
    var left = 20;
    var opacity = 1;
    var obj = setInterval(function () {
        fontSize += 10;
        top -= 10;
        left += 5;
        opacity -= 0.2;
        tag.style.fontSize = fontSize + 'px';
        tag.style.top = top + 'px';
        tag.style.left = left + 'px';
        tag.style.opacity = opacity;
        if(opacity < 0){
            // 关闭定时器
            clearInterval(obj);
            $(tag).remove();
        }
    },90);
}
console.log($('.bottom'));
$('.bottom').click(function () {
    console.log(111);
    $(window).scrollTop(0);
})
