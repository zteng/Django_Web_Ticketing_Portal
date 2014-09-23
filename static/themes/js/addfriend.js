/* check if elements in array have duplicates*/
function hasDuplicates(array) {
    var table = {};
    for (var i = 0; i < array.length; ++i) {
        var value = array[i];
        if (Object.prototype.hasOwnProperty.call(table, value)) {
            return true;
        }
        table[value] = true;
    }
    return false;
}

$(document).ready(function(){
    var next = 1;
	var friendlist = []
	for (var i = 0; i < $("#friendlist").children('option').length;i++) {
		friendlist.push($("#friendlist").children('option').eq(i).text());
	}
	
	$(".add-more").click(function(e){
	    var inputs = document.getElementsByClassName('form-control');
		/* check if the friend name user input is correct*/
	    for (var i = 0; i < inputs.length; i++) {
			var count = 0;
			for (var k = 0; k < friendlist.length; k++) {
				if (inputs[i].value == friendlist[k]) {
					count += 1;
				}
			}
			if (count == 0 ){
				alert('Added friend is not in the list of friend. Enter again!');
			}
	    }
		/* check if the friend name appear twice in the inputs*/
		input_values = []
		for (var j = 0; j < inputs.length; j++) {
			input_values.push(inputs[j].value);
		}
		if (hasDuplicates(input_values) == true) {
			alert('Can not have same member twice or more');
		}
	});
	
    $(".add-more").click(function(e){
        e.preventDefault();
        var addto = "#field" + next;
        var addRemove = "#field" + (next);
        next = next + 1;
        var newIn = '<input class="input form-control" placeholder="Add friend" id="field' + next + '" name="field' + '" type="text">';
        var newInput = $(newIn);
        var removeBtn = '<button id="remove' + (next - 1) + '" class="btn btn-danger remove-me" >-</button></div><div id="field">';
        var removeButton = $(removeBtn);
        $(addto).after(newInput);
        $(addRemove).after(removeButton);
        $("#field" + next).attr('data-source',$(addto).attr('data-source'));
        $("#count").val(next);  
        
            $('.remove-me').click(function(e){
                e.preventDefault();
                if (this.id.length == 7) {
                    var fieldNum = this.id.charAt(this.id.length-1);
                    var fieldID = "#field" + fieldNum;
				}
				else {
					var fieldNum1 = this.id.charAt(this.id.length-2);
					var fieldNum2 = this.id.charAt(this.id.length-1);
					var fieldID = "#field" + fieldNum1 + fieldNum2;                    
                }
                $(this).remove();
                $(fieldID).remove();
            });
			$("#"+newInput.attr('id')).autocomplete({
				source: friendlist
				});
    }); 
});