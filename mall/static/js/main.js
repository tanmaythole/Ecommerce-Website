

// Cart
$(document).ready(function(){
    url = new URL(window.location.href.toString());
    if(url.searchParams.get("sort-by")!=null){
        $("#"+url.searchParams.get("sort-by")).attr('checked', true);
    }

    if(url.searchParams.get("min")!=null){
        $("#input-left").val(url.searchParams.get("min"));
        setLeftValue();
    }
    if(url.searchParams.get("max")!=null){
        $("#input-right").val(url.searchParams.get("max"));
        setRightValue();
    }
    calculation();
});
function calculation(){
    subTotal = 0;
    discnt = 0;
    totalAmt = 0;
    shipping = 0;
    cart = $('.cart-product-container');
    jQuery.each(cart, function(e){
        id = cart[e].id;
        price = $('#'+id+" .price").text().split(" ");
        quantity = parseInt($('#'+id+' #quantity').text()) || $('#'+id+' #quantity').val();
        
        if (!quantity) {
            quantity = 1;
        }
        subTotal += parseInt(price[2].replace("₹", ""))*quantity;
        discnt += parseInt(price[2].replace("₹", ""))*quantity - parseInt(price[0].replace("₹", ""))*quantity;
    });
    $('.subtotal').text(['₹', subTotal].join(''));
    $('.discount').text(['- ', '₹', discnt].join(''));
    if(subTotal<500 && subTotal>0){
        shipping = 50;
    }
    else{
        shipping = 0;
    }
    $('.shipping').text(['₹', shipping].join(''));
    $('.totalamt').text(["₹",(subTotal-discnt+shipping)].join(''));

}

// increment cart product value
$('.btn-incr').on('click', function(e){
    id = e.target.parentElement.parentElement.parentElement.id;

    max = parseInt($('#'+id+' .btn-incr').attr('max'));
    quan = $('#'+id+' #quantity');
    quan.text(parseInt(quan.text())+1);
    $.ajax({
        url: "/cart/",
        type: "POST",
        data: {
            name: 'updateCart',
            product_id: id,
            quantity: quan.text(),
            csrfmiddlewaretoken: $('#'+id+' input[name=csrf]').val()
        },
        success: function(data){
            
        }, 
        error: function(data){
            alert("Something Went Wrong!");
        }
    });
    if(quan.text()>=max){
        $('#'+id+' .btn-incr').attr('disabled', 'true');
    }
    if(quan.text()>1){
        $('#'+id+' .btn-decr').removeAttr('disabled');
    }
    calculation();
});

// decrement cart product value
$('.btn-decr').on('click', function(e){
    id = e.target.parentElement.parentElement.parentElement.id;
    
    max = parseInt($('#'+id+' .btn-incr').attr('max'));
    quan = $('#'+id+' #quantity');
    quan.text(parseInt(quan.text())-1);
    $.ajax({
        url: "/cart/",
        type: "POST",
        data: {
            name: 'updateCart',
            product_id: id,
            quantity: quan.text(),
            csrfmiddlewaretoken: $('#'+id+' input[name=csrf]').val()
        },
        success: function(data){
            
        }, 
        error: function(data){
            alert("Something Went Wrong!");
        }
    });
    if(quan.text()==1){
        $('#'+id+' .btn-decr').attr('disabled', 'true');
    }
    if(quan.text()<max){
        $('#'+id+' .btn-incr').removeAttr('disabled');
    }
    calculation();
});


// Increment checkout product quantity
$('.btn-incr-prod').on('click', function(e){
    e.preventDefault();
    id = e.target.parentElement.parentElement.parentElement.id;

    max = parseInt($('#'+id+' .btn-incr-prod').attr('max'));
    quan = $('#'+id+' #quantity');
    quan.val(parseInt(quan.val())+1);

    if(quan.val()>=max){
        $('#'+id+' .btn-incr-prod').attr('disabled', 'true');
    }
    if(quan.val()>1){
        $('#'+id+' .btn-decr-prod').removeAttr('disabled');
    }
    calculation();
});

// Decrement Checkout product quantity
$('.btn-decr-prod').on('click', function(e){
    id = e.target.parentElement.parentElement.parentElement.id;
    
    max = parseInt($('#'+id+' .btn-incr-prod').attr('max'));
    quan = $('#'+id+' #quantity');
    quan.val(parseInt(quan.val())-1);
    
    if(quan.val()==1){
        $('#'+id+' .btn-decr-prod').attr('disabled', 'true');
    }
    if(quan.val()<max){
        $('#'+id+' .btn-incr-prod').removeAttr('disabled');
    }
    calculation();
});

// Add to Cart
$(".add-to-cart").click(function(e){
    id = e.target.parentElement.id;
    // console.log(id);
    $("#"+id+" .add-to-cart").text("GOING TO CART");
    $.ajax({
        url: "/cart/",
        type: "POST",
        data: {
            name: 'addToCart',
            product_id: id,
            quantity: 1,
            csrfmiddlewaretoken: $('#'+id+' input[name=csrf]').val()
        },
        success: function(data){
            if(data){
                window.location = '/cart/';
            }
        }, 
        error: function(data){
            alert("Something Went Wrong!");
        }
    });
});

// Remove Poduct from Cart
$(".remove-prod-from-cart").click(function(e){
    id = e.target.parentElement.parentElement.parentElement.id;
    // console.log(id);
    $.ajax({
        url: "/cart/",
        type: "POST",
        data: {
            name: 'removeProd',
            product_id: id,
            csrfmiddlewaretoken: $('#'+id+' input[name=csrf]').val()
        },
        success: function(data){
            if(data){
                alert("Cart Updated");
            }
        }, 
        error: function(data){
            alert("Something Went Wrong!");
        }
    });
});


// Slider
var inputLeft = document.getElementById("input-left");
var inputRight = document.getElementById("input-right");

var thumbLeft = document.querySelector(".slider > .thumb.left");
var thumbRight = document.querySelector(".slider > .thumb.right");
var range = document.querySelector(".slider > .range");

function setLeftValue() {
	var _this = inputLeft,
		min = parseInt(_this.min),
		max = parseInt(_this.max);

	_this.value = Math.min(parseInt(_this.value), parseInt(inputRight.value) - 1);
	var percent = ((_this.value - min) / (max - min)) * 100;

    thumbLeft.style.left = percent + "%";
	range.style.left = percent + "%";
    $("#min-value").val("₹"+inputLeft.value);

}
setLeftValue();

function setRightValue() {
    var _this = inputRight,
    min = parseInt(_this.min),
    max = parseInt(_this.max);
    
	_this.value = Math.max(parseInt(_this.value), parseInt(inputLeft.value) + 1);
    // console.log(_this.value);
    

	var percent = ((_this.value - min) / (max - min)) * 100;
    
	thumbRight.style.right = (100 - percent) + "%";
	range.style.right = (100 - percent) + "%";
    $("#max-value").val("₹"+inputRight.value);

}
setRightValue();

inputLeft.addEventListener("input", setLeftValue);
inputRight.addEventListener("input", setRightValue);

inputLeft.addEventListener("mouseover", function() {
	thumbLeft.classList.add("hover");
});
inputLeft.addEventListener("mouseout", function() {
	thumbLeft.classList.remove("hover");
});
inputLeft.addEventListener("mousedown", function() {
	thumbLeft.classList.add("active");
});
inputLeft.addEventListener("mouseup", function() {
	thumbLeft.classList.remove("active");
});

inputRight.addEventListener("mouseover", function() {
	thumbRight.classList.add("hover");
});
inputRight.addEventListener("mouseout", function() {
	thumbRight.classList.remove("hover");
});
inputRight.addEventListener("mousedown", function() {
	thumbRight.classList.add("active");
});
inputRight.addEventListener("mouseup", function() {
	thumbRight.classList.remove("active");
});

$("#input-left").on("change",function(){
    window.location = window.location.pathname + "?min=" + $(this).val() + "&&max=" + $("#input-right").val();
});
$("#input-right").on("change",function(){
    window.location = window.location.pathname + "?min=" + $("#input-left").val() + "&&max=" + $(this).val();
});




// Category subcategory wise product list
// sort by
$("input[name=sort-by]").on("change", function(e){
    window.location = window.location.pathname+"?sort-by="+e.target.id
});




