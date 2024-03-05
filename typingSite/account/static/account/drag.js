const track = document.querySelector('.track');
const arrow = document.querySelector('.arrow');
window.onmousedown = e => {
    track.dataset.downAt = e.clientX;

}
window.onmousemove = e => {
    if(track.dataset.downAt === "0") return;
    const mousedelta = parseFloat(track.dataset.downAt) - e.clientX;
    const maxdelta = window.innerWidth;
    let percent = mousedelta / maxdelta * -100;
    percent += parseFloat(track.dataset.prev);
    if(percent < 0) percent = 0;
    if(percent > 100) percent = 100;
    track.dataset.curr = percent;
    track.style.transform = `translate(-${percent}%, 50%)`;
    arrowpercent = 20 - (percent ) * 20 / 100;
    // console.log(arrowpercent);
    arrow.style.opacity = `${arrowpercent / 100}`;
}
window.onmouseup = e => {
    track.dataset.downAt = 0;
    track.dataset.prev = track.dataset.curr;
}