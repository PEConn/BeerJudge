__author__ = 'seneda'
import beerParser

a = ['Becks Staropramen Budweiser Sol Desperados Newcastle Brown Ale Birra Moretti Erdinger Efes Peroni Corona',
(u'Large Breakfast', u'1463 cal fried eggs, bacon, sausages, baked beans, hash browns, mushroom, tomato, slices of toast'),
(u'Traditional Breakfast', u'867 cal fried egg, bacon, sausage, baked beans, hash browns, tomato, slice of toast'),
(u'Large Vegetarian Breakfast', u'1378 cal fried eggs, vegetarian sausages, baked beans, hash browns, mushroom, tomato, slices of toast'),
(u'Vegetarian Breakfast', u'984 cal fried eggs, vegetarian sausage, baked beans, hash browns, mushroom, tomato, slice of toast'),
(u"Children's Breakfast", u'508 cal suitable for children aged 10 & under fried egg, bacon, sausage, baked beans, hash brown'),
(u'Breakfast Wrap', u'681 cal fried egg, bacon, sausage, hash brown, cheese. Also available as a vegetarian option'),
(u'Breakfast Bloomer Sandwich', u'653 cal sausage, bacon, fried egg'),
(u'Breakfast Roll', u'Choose\u200b from: bacon 420 cal; sausage 509 cal vegetarian sausage'),
(u'Pancakes', u'683 cal topped w/ bacon, maple-flavour syrup without bacon. 5%'),
(u'Moma! Porridge', u'5% strawberry & blueberry compote. 311 cal or honey & banana'),
(u'Eggs Benedict', u'573 cal two poached eggs, on an english muffin w/ wiltshire cured ham, hollandaise sauce')]


r = beerParser.start(a)
print r