"""
Local Utilities can be registered on subclasses of grok.Site using
grok.local_utility:

  >>> cave = SpikyCave()
  >>> getRootFolder()['cave'] = cave

  >>> from zope import component
  >>> from zope.component.hooks import getSite, setSite
  >>> setSite(cave)

  >>> club = component.getUtility(IClub)
  >>> IClub.providedBy(club)
  True
  >>> isinstance(club, SpikyClub)
  True

  >>> names = list(cave.getSiteManager().keys())
  >>> len(names)
  1

  >>> print(names[0])
  SpikyClub

"""
import grokcore.site
from zope import interface


class IClub(interface.Interface):
    pass


@interface.implementer(IClub)
class Club(grokcore.site.LocalUtility):
    pass


@interface.implementer(IClub)
class SpikyClub(grokcore.site.LocalUtility):
    pass


class Cave(grokcore.site.Site):
    grokcore.site.local_utility(Club)


class SpikyCave(Cave):
    grokcore.site.local_utility(SpikyClub)
