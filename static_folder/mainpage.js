var myIndex = 0;
carousel();

function carousel() {
    var i;
    var x = document.getElementsByClassName("mySlides");
    for (i = 0; i < x.length; i++) {
       x[i].style.display = "none";
    }
    myIndex++;
    if (myIndex > x.length) {myIndex = 1}
    x[myIndex-1].style.display = "block";
    setTimeout(carousel, 2000); // Change image every 2 seconds
}
// function image() {
//     if parsed_event_dictionary['events'] is "concerts":
//         print <img src="http://pa1.narvii.com/6461/57d12880e007e56dc1e43bd99393ed8a6f3166c0_hq.gif">
// }
