demo = document.querySelector('#demo');
demo.innerHTML = 'from js file';
console.log("am working")
image = document.querySelector('.cover-img')





const getRamdomImg = () => {
    sources = ["/static/images/cover2.jpg", "/static/images/cover1.jpg"];
    function get_random (list) {
        return list[Math.floor((Math.random()*list.length))];
      }
    image.src =  get_random(sources);
    

}