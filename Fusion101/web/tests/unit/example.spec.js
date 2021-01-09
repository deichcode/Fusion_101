import { shallowMount } from '@vue/test-utils'
import TutorialsOverview from "@/views/TutorialsOverview";

describe('TutorialsOverview.vue', () => {
  xit('renders props.msg when passed', () => {
    const msg = 'new message'
    const wrapper = shallowMount(TutorialsOverview, {
      props: { msg }
    })
    expect(wrapper.text()).toMatch(msg)
  })
})
