<script lang="ts" setup></script>

<template>
  <n-layout-footer class="footer" position="absolute">
    <div class="left">
      <div class="logo" @click="$router.push('/')">
        <SvgIcon name="logo"></SvgIcon>
      </div>
      <div class="rights">2024. All rights reserved.</div>
    </div>
    <div class="center">
      <div class="links">
        <a href="#" target="_blank">Privacy Policy</a>
        <a href="#" target="_blank">Cookie Policy</a>
      </div>
    </div>
    <div class="right">
      <div class="follow">Follow US</div>
      <div class="social">
        <a href="https://t.me/Balance_Fun" target="_blank">
          <SvgIcon name="telegram"></SvgIcon>
        </a>
        <a href="https://discord.com/invite/balance-fun" target="_blank">
          <SvgIcon name="discord"></SvgIcon>
        </a>
        <a href="https://x.com/Balance_Fun" target="_blank">
          <SvgIcon name="x"></SvgIcon>
        </a>
      </div>
    </div>
  </n-layout-footer>
</template>

<style lang="scss" scoped>
.footer {
  display: flex;
  width: 100%;
  padding: 40px 100px;
  justify-content: space-between;
  align-items: flex-end;
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  background: #000;
  z-index: 9;

  .left {
    display: flex;
    width: 228.15px;
    height: 100px;
    flex-direction: column;
    align-items: flex-start;
    gap: 32px;
    flex-shrink: 0;

    .svg-icon {
      width: 139.5px;
      height: 39.997px;
      flex-shrink: 0;
      cursor: pointer;
    }

    .rights {
      color: var(--color-text-secondary);

      /* Labels/S/Light */
      font-family: Sora;
      font-size: 12px;
      font-style: normal;
      font-weight: 300;
      line-height: 16px; /* 133.333% */
    }
  }

  .center {
    display: flex;
    align-items: flex-end;

    .links {
      display: flex;
      align-items: center;
      gap: 80px;

      a {
        color: var(--color-text-secondary, #888);

        /* Labels/S/Light */
        font-family: Sora;
        font-size: 12px;
        font-style: normal;
        font-weight: 300;
        line-height: 16px; /* 133.333% */
        cursor: pointer;
        text-decoration: none;

        &:hover {
          color: rgba(#888888, 0.85);
        }

        &:active {
          color: rgba(#888888, 0.75);
        }
      }
    }
  }

  .right {
    display: flex;
    width: 168px;
    flex-direction: column;
    align-items: flex-end;
    gap: 32px;
    flex-shrink: 0;

    .follow {
      color: #fff;
      text-align: right;

      /* Labels/S/Light */
      font-family: Sora;
      font-size: 12px;
      font-style: normal;
      font-weight: 300;
      line-height: 16px; /* 133.333% */
      opacity: 0.3;
    }

    .social {
      display: flex;
      align-items: center;
      gap: 24px;

      a {
        display: flex;
        width: 40px;
        height: 40px;
        padding: 10px;
        justify-content: center;
        align-items: center;
        gap: 10px;
        text-decoration: none;
        cursor: pointer;

        .svg-icon {
          width: 24px;
          height: 24px;
          color: #fff;

          &:hover {
            opacity: 0.85;
          }

          &:active {
            opacity: 0.75;
          }
        }
      }
    }
  }
}

@media (max-width: 1920px) {
  .footer {
    padding-left: clamp(64px, 4.44vw, 100px);
    padding-right: clamp(64px, 4.44vw, 100px);
  }
}
</style>
