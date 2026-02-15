javascript:(function(){
  const tag='audreyevans-20';
  const links=document.querySelectorAll('a[href*="amazon.com"]');
  let count=0;
  links.forEach(link=>{
    const url=new URL(link.href);
    url.searchParams.set('tag',tag);
    link.href=url.toString();
    count++;
  });
  alert(`Added affiliate tag to ${count} Amazon links!`);
})();
