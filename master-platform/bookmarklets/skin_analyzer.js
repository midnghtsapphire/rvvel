javascript:(function(){
  const images=document.querySelectorAll('img');
  if(images.length===0){
    alert('No images found on this page.');
    return;
  }
  const firstImg=images[0].src;
  const apiUrl=`https://api.projectface.com/analyze?image=${encodeURIComponent(firstImg)}`;
  fetch(apiUrl).then(r=>r.json()).then(data=>{
    alert(`Skin Analysis: ${JSON.stringify(data)}`);
  }).catch(e=>alert('Error analyzing image'));
})();
