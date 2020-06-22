using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace DailyHelpers.Mvvm
{
  public static class ObservableCollectionExtensions
  {
    public static void AddRangeNew<T>(this ObservableCollection<T> c, IEnumerable<T> items)
    {
      c.Clear();
      foreach (var item in items)
        c.Add(item);
    }
    public static void AddRangeNew<T>(this ObservableCollection<T> c, List<T> items)
    {
      c.Clear();
      items.ForEach(x => c.Add(x));
    }
  }
}
