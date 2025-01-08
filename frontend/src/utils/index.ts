import { NSpin } from 'naive-ui'
import iconSuccess from '@/assets/images/success.svg'
import iconArrowRight from '@/assets/images/arrow-right.svg'
import iconFail from '@/assets/images/fail.svg'

const formatAddress = (address: string) => {
  return `${address.slice(0, 5)}...${address.slice(-3)}`
}

const formatAmount = (number: number | string) => {
  if (!number) return '--'
  return (parseFloat(number + '') + '').replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * 格式化数字为带单位的字符串
 * @param amount 数字
 * @returns 带单位的字符串
 */
const formatAmountWithUnit = (amount: number) => {
  if (amount >= 1_000_000_000) {
    return `${(amount / 1_000_000_000).toFixed(2)}b`
  } else if (amount >= 1_000_000) {
    return `${(amount / 1_000_000).toFixed(2)}m`
  } else if (amount >= 1_000) {
    return `${(amount / 1_000).toFixed(2)}k`
  } else {
    return amount.toString()
  }
}

// 创建token进度通知
const progressNotify = () => {
  document.body.style.setProperty('--notification-border-color', '#fff')
  return window.$notification.create({
    content: () =>
      h('div', { class: 'content-wrapper' }, [
        h('div', { class: 'content' }, [h('div', { class: 'title' }, 'Interaction in progress...')])
      ]),
    duration: 500000,
    closable: false,
    keepAliveOnHover: true,
    avatar: () => h(NSpin, { size: 24, style: '--n-color: var(--notification-border-color)' })
  })
}

// 创建token成功通知
const successNotify = (callback: () => void) => {
  document.body.style.setProperty('--notification-border-color', '#00a878')
  return window.$notification.create({
    content: () =>
      h('div', { class: 'content-wrapper' }, [
        h('div', { class: 'content' }, [
          h('div', { class: 'title' }, 'Created New Coin'),
          h('div', { class: 'desc' }, 'Click to View it')
        ]),
        h(
          'div',
          {
            class: 'action',
            onClick: callback
          },
          [h('img', { src: iconArrowRight })]
        )
      ]),
    duration: 5000,
    closable: false,
    keepAliveOnHover: true,
    avatar: () => h('img', { src: iconSuccess })
  })
}

/**
 * 创建简单的成功或者失败通知
 * @param title 通知内容
 * @param status 通知状态
 * @returns
 */
const simpleNotify = (title: string, status: 'success' | 'fail' = 'success') => {
  const color = status === 'success' ? '#00a878' : '#DA4354'
  const icon = status === 'success' ? iconSuccess : iconFail
  document.body.style.setProperty('--notification-border-color', color)
  return window.$notification.create({
    content: () =>
      h('div', { class: 'content-wrapper' }, [
        h('div', { class: 'content' }, [h('div', { class: 'title' }, title)])
      ]),
    duration: 5000,
    closable: false,
    keepAliveOnHover: true,
    avatar: () => h('img', { src: icon })
  })
}

export {
  formatAddress,
  formatAmountWithUnit,
  formatAmount,
  progressNotify,
  successNotify,
  simpleNotify
}
