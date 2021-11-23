import { Observable } from 'rxjs';
import { debounceTime } from 'rxjs/operators';

const targetDOM = document.body;

const observeOnMutation = (target, config): Observable<MutationRecord[]> => {
  return new Observable((observer) => {
    const mutation = new MutationObserver((mutations, instance) => {
      observer.next(mutations);
    });
    mutation.observe(target, config);

    const unsubscribe = () => {
      mutation.disconnect();
    };
    return unsubscribe;
  });
}

const mutationObservable = observeOnMutation(targetDOM, { attributes: true, subtree: true })
  .pipe(
    debounceTime(200),
  ).subscribe((mutations) => {
    // do somethings...
  });