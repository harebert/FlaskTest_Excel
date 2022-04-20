// JavaScript Document
<script>
	
	$(document).ready(function(){
		  $(".scoreBut").click(
				function(){
				var button=$(this)
				
				var id_=button.attr("id").split("_")[1]
				console.log("this is add"+ id_)
				var temp = document.createElement("form");
				 temp.action = "http://ai.sfls.cn:5050/seeRelative";
				 //temp.action = "http://localhost:5050/seeRelative";
				 temp.method = "post";
				 temp.style.display = "none";
				var params = {
						"id_":id_,
						"action":button.attr("id").split("_")[0]
						
					 };
				 for (var x in params) {
				  var opt = document.createElement("textarea");
				  opt.name = x;
				  opt.value = params[x];
				  temp.appendChild(opt);
				 }

				 document.body.appendChild(temp);
				 temp.submit();

				 return temp;
			 		
				}
		
		);

			$('#myModal').on('show.bs.modal', function (event) {
				  var button = $(event.relatedTarget) // Button that triggered the modal
				  var recipient = button.data('url') // Extract info from data-* attributes
				  
				  console.log(recipient)
				  var modal = $(this)
				  modal.find('.modal-title').text('预览')
					//modal.find('.modal-body').text("<iframe width='500' height='440' frameborder='0' src='"+recipient+"'></iframe>")
				var iframe=$(this).find('.modal-body').find('.frame')
				iframe.attr("src",recipient)
//				iframe.setAttribute("src")=recipient
				iframe.attr("frameborder",'0')
				iframe.attr("width",'500')
				iframe.attr("height",'600')
				//$(this).find('.modal-body').append(iframe)
				var aLink=$(this).find('.modal-footer').find('.frameLink')
				aLink.attr("href",recipient)
				
				});
});

	
	</script>
