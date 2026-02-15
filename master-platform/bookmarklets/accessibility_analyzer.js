javascript:(function(){
  const issues=[];
  document.querySelectorAll('img').forEach(img=>{
    if(!img.alt||img.alt.trim()===''){
      issues.push({type:'Missing alt text',element:img});
    }
  });
  document.querySelectorAll('a').forEach(a=>{
    if(!a.textContent.trim()&&!a.getAttribute('aria-label')){
      issues.push({type:'Empty link',element:a});
    }
  });
  alert(`Found ${issues.length} accessibility issues. Check console for details.`);
  console.log('Accessibility Issues:',issues);
})();
