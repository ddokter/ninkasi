$(document).ready(function() {

  $(".listingfilter").on('keyup', function(e) {

    var li;
    var text = $(e.target).val().toLowerCase();
    var listing = $(e.target).parents(".listing").eq(0);

    //if(text.length < 3) {
    //  return false;
    //}

    if (!text) {
      listing.find(".list-group-item").show();
    } else {

      listing.find(".list-group-item").each(function(idx, elt) {

	li = $(elt);

	if (li.text().toLowerCase().indexOf(text) == -1) {
	  li.hide();
	} else {
	  li.show();
	}
      });
    }
  });

  $(".listingfilter").submit(function(e) {

    var form = $(e.target);
    var listing = form.parents(".listing").eq(0);
    var li;
    var text = form.find("[name=filter]").val().toLowerCase();

    if (!text) {
      listing.find(".list-group-item").show("slow");
    } else {

      listing.find(".list-group-item").each(function(idx, elt) {

	li = $(elt);

	if (li.text().toLowerCase().indexOf(text) == -1) {
	  li.hide("slow");
	} else {
	  li.show("slow");
	}
      });
    }

    e.preventDefault();

    return false;
  });

    /* Submit modal forms AJAX style */
    $("form.inline").submit(function(e) {

	var form = $(e.target);

	var modal = form.parents("div.modal");

	$.ajax(form.attr("action"),
               {type: form.attr("method") || "POST",
		data: form.serialize(),
		success: function(data, status, xhr) {

		    if (xhr.status == 202) {
			modal.find(".modal-body").replaceWith($(data).find(
			    ".modal-body"));
			modal.trigger("modal_action_show");
		    } else {
			modal.modal('hide');
		    }
		}
               });

	e.preventDefault();

	return false;
    });
});
