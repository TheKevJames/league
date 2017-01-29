from __future__ import division

import math

import league_utils.models as models
from . import gold


class GoldItemsSupport(object):
    def __init__(self, game_minutes=30):
        self.times = list(range(game_minutes * 60 + 1))

        self._adc_farm_rate = 0.85      # ADC gets n% of farm
        self._ranged_support = True
        self._support_farm_rate = 0.7   # Support hits relic shield at n% speed
        self._support_item_lag = 50     # Amount of extra gold when upgrading
        self._support_poke_rate = 0.75  # Support pokes at n% speed

        self.map = models.Map(11)  # SR
        self.lane = models.Lane('bot')

        self.other_items = 50  # pot
        self.item_blue = models.Item(3303)
        self.item_blue_upgrade = models.Item(3098)
        self.item_green = models.Item(3302)
        self.item_green_upgrade = models.Item(3097)
        self.item_yellow = models.Item(3301)
        self.item_yellow_upgrade = models.Item(3096)

        self._passive_gold = list()
        self._blue = list()
        self._green = list()
        self._yellow = list()

        self.line_blue = None
        self.line_green = None
        self.line_yellow = None

        import matplotlib.pyplot as plot
        self.plot = plot
        self.axes = None

        self.update_passive_gold()
        self.update_blue()
        self.update_green()
        self.update_yellow()

    def update_adc_farm_rate(self, value):
        self._adc_farm_rate = value

        self.do_updates()

    def update_ranged_support(self, value):
        self._ranged_support = value == 'Ranged'

        self.do_updates()

    def update_support_farm_rate(self, value):
        self._support_farm_rate = value

        self.do_updates(blue=False, yellow=False)

    def update_support_item_lag(self, value):
        self._support_item_lag = value

        self.do_updates()

    def update_support_poke_rate(self, value):
        self._support_poke_rate = value

        self.do_updates()

    def update_passive_gold(self):
        self._passive_gold = [
            self.map.starting_gold +
            gold.passively_generated(self.map.gold_per_ten, time) +
            gold.passively_generated_bandit(
                self.lane, self._ranged_support, time,
                farm_rate=self._adc_farm_rate,
                poke_rate=self._support_poke_rate)
            for time in self.times]

    def update_blue(self):
        item = self.item_blue

        self._blue = []
        for i, time in enumerate(self.times):
            item_gold = item.effects.gold_at_time(
                time, lane=self.lane,
                support_poke_rate=self._support_poke_rate)
            current_gold = self._passive_gold[i] + item_gold
            if current_gold > self.item_blue_upgrade.cost + \
                    self.other_items + self._support_item_lag:
                item = self.item_blue_upgrade

            self._blue.append(current_gold)

    def update_green(self):
        item = self.item_green

        self._green = []
        for i, time in enumerate(self.times):
            item_gold = item.effects.gold_at_time(
                time, lane=self.lane,
                support_farm_rate=self._support_farm_rate)
            current_gold = self._passive_gold[i] + item_gold
            if current_gold > self.item_green_upgrade.cost + \
                    self.other_items + self._support_item_lag:
                item = self.item_green_upgrade

            self._green.append(current_gold)

    def update_yellow(self):
        item = self.item_yellow

        self._yellow = []
        for i, time in enumerate(self.times):
            item_gold = item.effects.gold_at_time(
                time, adc_farm_rate=self._adc_farm_rate, lane=self.lane)
            current_gold = self._passive_gold[i] + item_gold
            if current_gold > self.item_yellow_upgrade.cost + \
                    self.other_items + self._support_item_lag:
                item = self.item_yellow_upgrade

            self._yellow.append(current_gold)

    def do_updates(self, blue=True, green=True, yellow=True):
        self.update_passive_gold()
        if blue:
            self.update_blue()
            self.line_blue.set_ydata(self._blue)
        if green:
            self.update_green()
            self.line_green.set_ydata(self._green)
        if yellow:
            self.update_yellow()
            self.line_yellow.set_ydata(self._yellow)
        largest_y = 1000 * math.ceil(
            max([self._blue[-1], self._green[-1], self._yellow[-1]]) / 1000)
        self.axes.set_ylim(0, largest_y)
        self.plot.draw()

    def render(self):
        _, self.axes = self.plot.subplots()
        self.plot.subplots_adjust(left=0.15, bottom=0.30)
        self.plot.title('Gold per Time')

        self.line_blue, = self.axes.plot(self.times, self._blue, color='b')
        self.line_green, = self.axes.plot(self.times, self._green, color='g')
        self.line_yellow, = self.axes.plot(self.times, self._yellow, color='y')
        self.axes.legend(["Spellthief's Edge", 'Relic Shield', 'Ancient Coin'],
                         loc='upper left')

        self.plot.xlabel('Time')
        ticks = range(0, self.times[-1] + 1, 60 * 5)
        self.plot.xticks(self.times, ['{}m'.format(t // 60) for t in ticks])
        self.axes.set_xticks(ticks)
        self.axes.set_xticks(range(0, self.times[-1] + 1, 60), minor=True)

        self.plot.ylabel('Gold')
        self.axes.set_ylim(0)

        self.axes.grid(which='minor', alpha=0.3)
        self.axes.grid(which='major', alpha=0.6)

        # ADC Farm Rate Slider
        adc_fr_axis = self.plot.axes([0.25, 0.19, 0.65, 0.03])
        slider_adc_farm_rate = self.plot.Slider(
            adc_fr_axis, 'ADC Farm Rate', 0.0, 1.0,
            valinit=self._adc_farm_rate)

        slider_adc_farm_rate.on_changed(self.update_adc_farm_rate)

        # Support Farm Rate Slider
        support_fr_axis = self.plot.axes([0.25, 0.14, 0.65, 0.03])
        slider_support_farm_rate = self.plot.Slider(
            support_fr_axis, 'Support Farm Rate', 0.0, 1.0,
            valinit=self._support_farm_rate)

        slider_support_farm_rate.on_changed(self.update_support_farm_rate)

        # Support Poke Rate Slider
        support_pr_axis = self.plot.axes([0.25, 0.09, 0.65, 0.03])
        slider_support_poke_rate = self.plot.Slider(
            support_pr_axis, 'Support Poke Rate', 0.0, 1.0,
            valinit=self._support_poke_rate)

        slider_support_poke_rate.on_changed(self.update_support_poke_rate)

        # Support Upgrade Item Lag Slider
        supp_uil_slider = self.plot.axes([0.25, 0.04, 0.65, 0.03])
        slider_support_upgrade_item_lag = self.plot.Slider(
            supp_uil_slider, 'Upgrade Item Lag', 0, 1000,
            valinit=self._support_item_lag)

        slider_support_upgrade_item_lag.on_changed(
            self.update_support_item_lag)

        # Support Ranged Toggle
        from matplotlib.widgets import RadioButtons
        support_r_axis = self.plot.axes([0.725, 0.325, 0.15, 0.15])
        buttom_support_ranged_toggle = RadioButtons(
            support_r_axis, ('Melee', 'Ranged'),
            active=int(self._ranged_support))

        buttom_support_ranged_toggle.on_clicked(self.update_ranged_support)

        self.plot.savefig('gold-items-support.png')
        self.plot.show()
