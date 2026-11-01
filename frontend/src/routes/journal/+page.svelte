<script>
    let myLogs = [
        { id: 1, place_name: 'Saxophone Pub & Restaurant', rating: '⭐⭐⭐⭐⭐', review: 'ดนตรีแจ๊สดีมาก แนะนำให้จองโต๊ะล่วงหน้าเพราะคนเต็มเร็วสุดๆ บรรยากาศโคตรคลาสสิก', date: '24 Oct 2026' },
        { id: 2, place_name: 'Havana Social', rating: '⭐⭐⭐⭐', review: 'ค็อกเทลอร่อย ทางเข้าลับตื่นเต้นดี แต่ช่วงดึกวันหยุดคนค่อนข้างแน่นไปหน่อย', date: '30 Oct 2026' }
    ];
</script>

<div class="mt-5 mb-6">
    <p class="is-size-7 has-text-weight-bold mb-1" style="color: #ccff00;">MY DIARY</p>
    <h1 class="title is-2 has-text-white mb-2">Journal</h1>
    <p class="has-text-grey">Journal of your experiences and reviews</p>
</div>

<div class="box mb-6" style="background-color: #1a1a1a; border: 1px dashed #333;">
    <p class="has-text-weight-bold mb-3" style="color: #ccff00;">+ Log a new experience</p>
    
    <!-- เอาช่อง Search ออก เปลี่ยนเป็นปุ่มสำหรับให้ User กดเพิ่มรีวิวเอง -->
    <button class="button is-small has-text-weight-bold" style="background-color: #ccff00; color: black;">
        Add Review
    </button>
</div>

<h2 class="title is-4 has-text-white mb-4">Recent Logs</h2>
<div class="columns is-multiline">
    {#each myLogs as log (log.id)}
        <div class="column is-6">
            <div class="card" style="background-color: #1a1a1a; border-radius: 12px; height: 100%;">
                <div class="card-content">
                    <div class="is-flex is-justify-content-space-between is-align-items-center mb-2">
                        <p class="title is-5 has-text-white mb-0">{log.place_name}</p>
                        <span class="has-text-grey-light is-size-7">{log.date}</span>
                    </div>
                    <p class="mb-3 is-size-6">{log.rating}</p>
                    <p class="content has-text-grey-light is-size-7" style="font-style: italic;">"{log.review}"</p>
                    <div class="buttons mt-4">
                        <button class="button is-small is-dark">Edit Log</button>
                        <button class="button is-small is-danger is-outlined">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    {/each}
</div>