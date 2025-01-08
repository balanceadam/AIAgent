<script lang="ts" setup>
// const router = useRouter()

// const goToLaunch = () => {
//   router.push('/launch')
// }
</script>
<template>
  <div class="page-view earn">
    <div class="comming-soon">
      <div class="content">
        <div class="title">COMING SOON</div>
        <div class="desc">
          Developers and designers are working intensively. How about you drink a cup of coffee and
          listen to a Beatles song first?
        </div>
      </div>
      <!-- <div class="button button-create" @click="goToLaunch">
        <span>Let's Create Token</span>
        <SvgIcon name="arrow-right" />
      </div> -->
    </div>
  </div>
</template>

<style>
.earn {
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: url(@/assets/images/bg-earn.png);
  background-size: cover;
  background-position: center;
  height: calc(100vh - 100px);

  .comming-soon {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 40px;

    .content {
      width: 468px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 24px;
      align-self: stretch;

      .title {
        color: #fff;
        text-align: center;

        /* Display1/Regular */
        font-family: Sora;
        font-size: 52px;
        font-style: normal;
        font-weight: 400;
        line-height: 64px; /* 123.077% */
      }

      .desc {
        color: #888;
        text-align: center;
        text-shadow: 0px 0px 36.4px #000;

        /* Paragraphs/XS/Light */
        font-family: Sora;
        font-size: 12px;
        font-style: normal;
        font-weight: 300;
        line-height: 20px; /* 166.667% */
        opacity: 0.7;
      }
    }
  }
}
</style>
