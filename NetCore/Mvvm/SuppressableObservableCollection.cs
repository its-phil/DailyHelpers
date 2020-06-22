using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.ComponentModel;
using System.Linq;

namespace DailyHelpers.Mvvm
{
  public class SuppressableObservableCollection<T> : ObservableCollection<T>
  {
    public bool SuppressEvents { get; private set; } = false;

    public SuppressableObservableCollection()
      : base()
    {
    }

    public SuppressableObservableCollection(IReadOnlyList<T> collection)
      : base()
    {
      AddRange(collection);
    }

    public void ReplaceCollectionEvent(T oldItem, T newItem)
    {
      OnCollectionChanged(new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Replace,
        new List<T> { newItem }, new List<T> { oldItem }));
    }

    protected override void OnCollectionChanged(NotifyCollectionChangedEventArgs e)
    {
      if (!SuppressEvents)
      {
        OnCollectionChangedMultiple(e);
      }
    }

    protected override void OnPropertyChanged(PropertyChangedEventArgs e)
    {
      if (!SuppressEvents)
      {
        base.OnPropertyChanged(e);
      }
    }

    public void AddRange(IEnumerable<T> items)
    {
      // Check if there are items to add in order to avoid exceptions 
      // when notifying the list event subscribers
      if (items.Count() > 0)
      {
        SuppressEvents = true;
        foreach (T item in items)
        {
          base.Add(item);
        }
        SuppressEvents = false;
        var newItems = items.ToList();
        OnCollectionChangedMultiple(new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Add, newItems));
        base.OnPropertyChanged(new PropertyChangedEventArgs("Count"));
      }
    }

    public void AddRange(IReadOnlyList<T> items)
    {
      // Check if there are items to add in order to avoid exceptions 
      // when notifying the list event subscribers
      if (items.Count > 0)
      {
        SuppressEvents = true;
        foreach (T item in items)
        {
          base.Add(item);
        }
        SuppressEvents = false;
        var newItems = items.ToList();
        OnCollectionChangedMultiple(new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Add, newItems));
        base.OnPropertyChanged(new PropertyChangedEventArgs("Count"));
      }
    }

    internal NotifyCollectionChangedEventHandler CollectionChangedDelegate;
    public override event NotifyCollectionChangedEventHandler CollectionChanged
    {
      add { CollectionChangedDelegate += value; }
      remove { CollectionChangedDelegate -= value; }
    }

    protected void OnCollectionChangedMultiple(NotifyCollectionChangedEventArgs e)
    {
      if (CollectionChangedDelegate != null)
      {
        foreach (var handler in CollectionChangedDelegate.GetInvocationList())
        {
          handler.DynamicInvoke(this, e);
        }
      }
    }

    public void AddRangeNew(IReadOnlyList<T> items)
    {
      SuppressEvents = true;
      Clear();
      if (items.Count > 0)
        AddRange(items);

      SuppressEvents = false;
    }

    public void AddRangeNew(IEnumerable<T> items)
    {
      SuppressEvents = true;
      Clear();
      if (items.Count() > 0)
        AddRange(items);

      SuppressEvents = false;
    }
  }
}
